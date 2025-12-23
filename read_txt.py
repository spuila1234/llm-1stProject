import pandas as pd

def to_dataframe(segments):
    df = pd.DataFrame(segments)
    df = df[["번호", "시작", "끝", "발화자", "대화 내용"]]
    df.columns = ["번호", "시작", "끝", "발화자", "대화 내용"]
    df["시작"] = df["시작"].astype(float)
    df["끝"] = df["끝"].astype(float)
    return df

def to_table_html(segments):
    df = to_dataframe(segments)

    html = df.to_html(index=False, escape=False)

    style = """
    <style>
      table {border-collapse: collapse; width: 100%;}
      th { text-align: center; padding: 8px; border: 1px solid #ddd; font-size: 13px;}
      td { padding: 8px; border: 1px solid #ddd; vertical-align: top; font-size: 13px; text-align: left;}
      /* Text 칼럼(마지막)만 좌측정렬 유지, 나머지 열은 가운데 정렬 */
      table thead th:nth-child(5),
      table tbody td:nth-child(5) { text-align: left; }
      /* 나머지 열 가운데 정렬 */
      table thead th:not(:nth-child(5)),
      table tbody td:not(:nth-child(5)) { text-align: center; }
      /* Text 열의 줄바꿈 허용 */
      td.Text { white-space: pre-wrap; word-break: break-word; text-align: left; }
    </style>
    """

    html = style + html
    return html


