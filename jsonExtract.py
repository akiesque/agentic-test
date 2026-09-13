import ollama

raw_table = """
Results of Operations (Php Mn)
Quarter on Quarter Year-on-Year
Q2 Q1 QoQ 30-Jun 30-Jun YoY
2026 2026 Change 2026 2025 Change
(%) (%)
Operating Revenues 46,955 45,706 3% 92,661 87,226 6%
Service Revenues 43,402 41,965 3% 85,367 80,188 6%
Mobile* 30,428 29,965 2% 60,393 57,073 6%
Home Broadband** 6,265 6,178 1% 12,443 11,708 6%
Corporate Data 5,910 5,135 15% 11,045 9,627 15%
Fixed line Voice 301 322 -7% 623 626 -1%
Others*** 498 365 37% 863 1,154 -25%
Non-Service Revenues 3,553 3,741 -5% 7,294 7,038 4%
Costs and Expenses 24,254 23,532 3% 47,786 45,086 6%
Cost of Sales 3,742 3,858 -3% 7,600 7,119 7%
Operating Expenses 20,512 19,674 4% 40,186 37,967 6%
EBITDA 22,701 22,174 2% 44,875 42,140 6%
EBITDA Margin 52.3% 52.8% - 52.6% 52.6% -
Depreciation 14,304 14,361 - 28,665 26,430 8%
EBIT 8,397 7,813 7% 16,210 15,710 3%
EBIT Margin 19.3% 18.6% - 19.0% 19.6% -
Non-Operating Income (Charges) (1,783) (1,286) 39% (3,069) (980) 213%
Net Income After Tax (NIAT) 5,485 5,554 -1% 11,039 12,437 -11%
Core Net Income 5,256 4,932 7% 10,188 10,431 -2%
"""

response = ollama.chat(
    model="qwen2.5:7b",
    options={
        "num_ctx": 8192
        },
    messages=[
        {
            "role": "user",
            "content": f"""Convert this financial table into JSON.

There are 19 line items in this table. You MUST process every single one - do not skip any, do not stop early, do not summarize.

Use this structure, repeated once per line item:
{{"Operating Revenues": {{"Q2 2026": "46,955", "Q1 2026": "45,706", "QoQ Change": "3%", "30-Jun 2026": "92,661", "30-Jun 2025": "87,226", "YoY Change": "6%"}}, "Service Revenues": {{...}}, ...continue for ALL remaining line items...}}

Return ONLY valid JSON containing all 19 line items. No explanation, no markdown code fences, no truncation.

Table:
{raw_table}"""
        }
    ]
)

print(response["message"]["content"])