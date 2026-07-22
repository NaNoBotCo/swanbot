from tools import get_ytd_stats as raw_ytd_stats
from utils import extract_tickers
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

llm = ChatOpenAI(temperature=0.92)

prompt_template = ChatPromptTemplate.from_template(
    """You are Black Swan, a stripper-quant. You tell the truth about stocks using this data:

    {stats}

    Now respond to the user's question, using only the information above. No guessing.
    If the stats are bearish, say so. If they're bullish, say so. If stats are missing, say so clearly.

    === USER INPUT ===
    {user_prompt}
    """
)

async def run_black_swan(user_prompt: str) -> str:
    tickers = extract_tickers(user_prompt)
    print("🧠 Detected tickers:", tickers)
    stats = ""

    if tickers:
        responses = []
        for t in tickers:
            try:
                stat = raw_ytd_stats.func(t)
                print(f"📊 Stats for {t}:\n{stat}\n")
                responses.append(stat)
            except Exception as e:
                print(f"❌ Error for {t}: {e}")
                responses.append(f"{t.upper()}: error fetching data")
        stats = "\n\n".join(responses)
    else:
        print("⚠️ No tickers found.")

    chain = prompt_template | llm | StrOutputParser()
    result = await chain.ainvoke({"user_prompt": user_prompt, "stats": stats})
    print("🖤 FINAL RESPONSE:\n", result, "\n")
    return result
