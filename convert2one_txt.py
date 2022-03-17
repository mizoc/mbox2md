#!/usr/bin/python3
import sys
from email.header import decode_header
import re
from pytz import timezone
from dateutil import parser
import mailbox
import base64
import cv2
import numpy as np

TIMEZONE = "Asia/Tokyo"


def main(filepath):
    mbox = mailbox.mbox(filepath)
    keys = mbox.keys()
    for key in keys:
        print(
            f"""

#######################################
No.{key}"""
        )

        mail_data = mbox.get(key)

        # date
        mail_date = re.findall("@xxx (.*)$", mail_data.get_from())[0]
        print(parser.parse(mail_date).astimezone(timezone(TIMEZONE)).strftime("Date(%Z):%Y/%b/%d (%a) %H:%M:%S"))

        # subject
        # print(mail_data)
        if mail_data["Subject"] is None:
            print("Subject:None")
        else:
            header = decode_header(mail_data["Subject"])
            # if type(header[0][0]) == str:
            if header[0][1] is None:
                print(f"Subject:{header[0][0]}")
            else:
                print(f"Subject:{header[0][0].decode(header[0][1], 'ignore')}")

        # mail addr
        try:
            print(f"From:{re.findall(' <(.*)>', mail_data['From'])[0]}")
        except:
            print(f"From:{mail_data['from']}")
        print("#######################################")

        i = 0
        for aa_msg in mail_data.walk():
            # print(aa_msg.get_content_type())

            # body
            # Referred to http://techu1999.sakura.ne.jp/python/category/%E3%83%A1%E3%83%BC%E3%83%AB%E5%87%A6%E7%90%86/
            if "text/plain" in aa_msg.get_content_type():
                if aa_msg.get_content_charset():
                    a_text = aa_msg.get_payload(decode=True).decode(aa_msg.get_content_charset(), "ignore")
                else:
                    if "charset=shift_jis" in str(aa_msg.get_payload(decode=True)):
                        # ひとまず シフトJISだけ特別対応。
                        a_text = aa_msg.get_payload(decode=True).decode("cp932", "ignore")
                    else:
                        print("** Cannot decode.Cannot specify charset ***" + msg.get("From"))
                print(a_text)

            # image どうせbase64だろ
            elif "image" in aa_msg.get_content_type():
                cv2.imwrite(
                    f"./attachments/{key}-{str(i)}.jpg",
                    cv2.imdecode(np.frombuffer(base64.b64decode(aa_msg.get_payload()), dtype=np.uint8), cv2.IMREAD_COLOR),
                )
                print(f"Attachment:{aa_msg.get_filename()}(./attachments/{key}-{i}.jpg)")

                i += 1


if __name__ == "__main__":
    # 引数でfile path指定する
    main(sys.argv[1])
