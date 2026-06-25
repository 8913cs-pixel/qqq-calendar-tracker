import yfinance as yf
import pandas as pd

ticker = yf.Ticker("QQQ")

expiries = ticker.options

results = []

for i in range(len(expiries) - 1):

    near_exp = expiries[i]
    far_exp = expiries[i + 1]

    near_chain = ticker.option_chain(near_exp)
    far_chain = ticker.option_chain(far_exp)

    near_calls = near_chain.calls
    far_calls = far_chain.calls

    near_puts = near_chain.puts
    far_puts = far_chain.puts

    for strike in range(650, 851, 5):

        try:

            near_call = near_calls.loc[
                near_calls["strike"] == strike
            ].iloc[0]

            far_call = far_calls.loc[
                far_calls["strike"] == strike
            ].iloc[0]

            near_call_mid = (
                near_call["bid"] + near_call["ask"]
            ) / 2

            far_call_mid = (
                far_call["bid"] + far_call["ask"]
            ) / 2

            call_calendar = (
                far_call_mid - near_call_mid
            )

        except:
            near_call_mid = None
            far_call_mid = None
            call_calendar = None

        try:

            near_put = near_puts.loc[
                near_puts["strike"] == strike
            ].iloc[0]

            far_put = far_puts.loc[
                far_puts["strike"] == strike
            ].iloc[0]

            near_put_mid = (
                near_put["bid"] + near_put["ask"]
            ) / 2

            far_put_mid = (
                far_put["bid"] + far_put["ask"]
            ) / 2

            put_calendar = (
                far_put_mid - near_put_mid
            )

        except:
            near_put_mid = None
            far_put_mid = None
            put_calendar = None

        results.append({
            "Near_Expiry": near_exp,
            "Far_Expiry": far_exp,
            "Strike": strike,
            "Near_Call_Mid": near_call_mid,
            "Far_Call_Mid": far_call_mid,
            "Call_Calendar": call_calendar,
            "Near_Put_Mid": near_put_mid,
            "Far_Put_Mid": far_put_mid,
            "Put_Calendar": put_calendar
        })

df = pd.DataFrame(results)

with pd.ExcelWriter(
    "QQQ_Calendar_Spreads.xlsx",
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Calendar_Spreads",
        index=False
    )

print("Excel file created.")
