import os
from dotenv import load_dotenv
import google.generativeai as genai
from telethon import TelegramClient
from datetime import datetime
import pytz
from consts import *

# Load environment variables from .env file
load_dotenv()

async def get_channel_id(client, channel_name):
    async for dialog in client.iter_dialogs():
        if dialog.name == channel_name:
            return dialog.id

async def get_todays_messages(client, channel_id):
    israel_timezone = pytz.timezone('Israel')
    today_israel = datetime.now(israel_timezone).date()

    messages = []
    async for message in client.iter_messages(channel_id):
        message_date_israel = message.date.astimezone(israel_timezone).date()

        if message_date_israel == today_israel:
            messages.append(message)
        else:
            break
    
    return messages

async def summarize(messages):
    # Access Google API key using os.environ
    google_api_key = os.environ.get('GOOGLE_API_KEY')

    # Check if API key is loaded
    if google_api_key is None:
        raise ValueError("Google API Key not found in .env file. Please set the 'GOOGLE_API_KEY' environment variable.")
    
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    israel_timezone = pytz.timezone('Israel')
    today_israel = datetime.now(israel_timezone).date()

    summary_end = '''**⚠️ הסיכום נכתב על ידי בינה מלאכותית ויכול להיות לא מדויק ואף שגוי לפעמים. להודעות המקוריות מוזמנים להיכנס לערוץ של עמית סגל @amitsegal. עם ישראל חי! לילה טוב 😴**'''
    prompt_text = f'''אני הולך לתת לך עכשיו את הטקסט של הודעות הטלגרם שעמית סגל שלח היום. הטקסט של ההודעות יהיה מופרד עם ###  בין כל הודעה. לאחר שקראת את הטקסט ועברת על התמונות:
    1. קרא את ההודעות וסווג אותן לפי רמת חשיבות (האם כדאי להכניס אותן לסיכום או לא).
    2. תכתוב סיכום של ההודעות שעמית סגל שלח היום. שים לב שאתה כותב את הסיכום בצורה מסודרת ומפריד בין "חדשות" שהן הודעות עובדתיות לבין ״פרשנויות״ של עמית סגל.
    3. אל תמציא עובדות אלא תכניס לסיכום רק מה שכתוב בהודעות
    4. תחזיר לי רק את הסיכום, שיתחיל במילים ״עמית סגל - סיכום יומי | ״  + התאריך של היום - {today_israel}. ויהיה מעוצב יפה לפי הפורמט של טלגרם (לדוגמא, ** משני צדדי מדגיש את המילה).
    5. בתחילת כל נקודה תשתמש בסימן ״-״
    6. בתוך הסימנים *** תופיע דוגמא להודעות וסיכום של יום מסוים. ההודעות הרלוונטיות של היום מופיעות בסוף.

    דוגמא:
    ***
    הודעות:
    ###
    צה״ל פועל כבר שעות בבית החולים שיפא בעקבות מידע על בכירי חמאס שפועלים ממנו. במהלך הלילה התנהלו חילופי אש במקום
    ###
    80 עצורים במקום, בפעולה שנמשכת כבר חמש שעות
    ###
    [Matan Kahana מתן כהנא (‎@MatanKahana‎) ב-X](https://x.com/matankahana/status/1769620807544717668?s=48&t=2vpQ0urqk2g-dl_6CbQ6kQ)
    עולה היום:

    https://x.com/matankahana/status/1769620807544717668?s=48&t=2vpQ0urqk2g-dl_6CbQ6kQ
    ###
    סיעת הימין הממלכתי יחד עם סיעת המחנה הממלכתי החליטו להטיל וטו על המשך קידום הצעת חוק שירותי הדת היהודיים (בחירות רבני עיר, רבנים אזוריים, רבני יישוב ורבי שכונות). 

    ח״כ זאב אלקין הודיע על כך ליו״ר הקואליציה, ח״כ אופיר כץ.
    ###

    ###
    מתן
    ###
    הנשיא הרצוג במכינת עלי: יש לי אמון מלא בצה״ל ובמפקדיו
    ###
    מתן נהרג בקרב בשיפא
    ###
    אולי אני חשדן אבל נראה שהוטו של המחנה הממלכתי על חוק הרבנים הוא בין היתר תג מחיר על כך שדרעי סירב להצעתם לחוק גיוס תמורת מועד לפיזור הכנסת, ואחר כך הידיעה דלפה.
    ###
    הודעה משותפת לדובר צה"ל ודוברות שב"כ:

    **במהלך פעילות לסיכול טרור בבית החולים שיפאא': צה״ל ושב״כ חיסלו את ראש מנהלת המבצעים בבטחון הפנים של ארגון הטרור חמאס**

    בעקבות מידע מודיעיני של שב"כ ואמ״ן על המצאות בכירי חמאס בבית החולים שיפאא׳, צה"ל ושב"כ יצאו הלילה למבצע מעצר ממוקד במסגרתו הכוחות חיסלו את המחבל, פאא׳ק מבחוח.

    מבחוח בתפקידו ראש מנהלת המבצעים בבטחון הפנים של ארגון הטרור חמאס. מבחוח אחראי בין היתר על סנכרון מנגנוני חמאס ברצועה בשגרה ובלחימה.

    מבחוח חוסל בחילופי אש עם הכוחות בעודו חמוש ומסתתר בתוך מתחם בבית החולים שיפאא׳ אשר ממנו פעל לקידום פעילות טרור. בחדר הסמוך למקום בו חוסל אותר אמל״ח רב.
    ###
    על אף מחאת סמוטריץ: 

    זה סבב המינויים בצבא

    https://IDFANC.activetrail.biz/ANC1803202456587
    ###
    ביידן ונתניהו ישוחחו היום אחרי חודש
    ###
    הקואליציה תקדם את חוק הרבנים למרות הוטו של גנץ וסער. הנימוק: גנץ הצביע נגד התקציב ונסע לחו״ל ללא אישור הממשלה

    נימוק מעשי יותר: ש״ס מתעקשת
    ###
    גלנט
    ###
    שופט העליון חאלד כבוב הציע להקל בעונשם של חשודים בטרור בשם השוויון - כי חבריהם שוחררו בעסקה עם החמאס.
    ###
    לפיד בישיבת הסיעה היום: מתנהל כרגע דיון מול אנשים בליכוד, יש לנו בעיה כל עוד גנץ ואייזנקוט בממשלה. הליכודניקים אומרים לנו מה אתה רוצה מהחיים שלנו, גדי ובני בממשלה וזה הופך אותה ללגיטימית וזה הופך את נתניהו ללגיטימי וזה מקשה להפיל אותה.
    ###
    הודעה משותפת לדובר צה"ל ודוברות שב"כ:

    צה״ל ושב״כ הרגו עד כה כ-20 מחבלים בהתקלויות בבית החולים שיפאא', ותפסו עשרות עצורים שנמצאים בשעות אלו בחקירה

    כוחות צה״ל ושב״כ, בהובלת אוגדה 162, צוות הקרב החטיבתי 401, וכוחות שייטת 13 ממשיכים לפעול בבית החולים שיפפא׳ לסיכול טרור באופן ממוקד.

    בבית החולים אותרו כספי טרור שיועדו לחלוקה לפעילי טרור של חמאס בתוך בית החולים. בנוסף, אותר בבית החולים אמצעי לחימה רבים. כוחות צה״ל ממשיכים בפעילות המבצעית ובסריקות במרחב.
    ###
    מיד: פירוט על שיחת ביידן נתניהו שעסקה ברפיח ובמצב בעזה
    ###
    נתניהו: הסיוע ההומניטרי הכרחי כדי להכניע את חמאס
    ###
    עוד מעט - ידיעה מסקרנת על פרס ישראל
    ###
    ובכן, מסתבר שלא רק איל ולדמן כבר נבחר כזוכה פרס ישראל אלא לא אחר מאשר הראשון לציון הרב יצחק יוסף.

    הרב זוכה בפרס ישראל לספרות תורנית, והפרס יוענק לו לאחר שקרא לרדת מהארץ אם יגוייסו תלמידי ישיבות. 

    וכך אם יתקיים הטקס ביום העצמאות הזה כפי שדורשים מהשר יקבל את הפרס הנחשב ביותר של מדינת ישראל מי שקרא לעזוב את המדינה.
    ###

    ###
    ישראל תשלח משלחת מדינית לוושינגטון להסביר את כוונותיה באשר לרפיח
    ###
    ארה״ב: מרוואן עיסא חוסל

    🇮🇱🇮🇱🇮🇱
    ###
    הודעה  מאת לשכת הראשון לציון הרב הראשי לישראל הרב יצחק יוסף : 

    ככל שיש ממש בפרסום על הכוונה להעניק לראשון לציון שליט״א את ׳פרס ישראל׳ בגין מפעלו התורני ועל אף שמדובר בהחלטה המבטאת 50 שנות יצירה הלכתית, הרי שלא זו העת ולא זו השעה. 
    בהתאם לכך מבקש כבוד הראשון לציון למסור:  **כי ״אילו היה ידוע לו על הגשתו כמועמד לקבלת ׳פרס ישראל׳ היה פועל למנוע זאת. אין זו שנה מתאימה לטקסים וחגיגות. ההוקרה היחידה של מדינה לאזרחיה, היא שמירה על בטחונם והוקרת החיילים המחרפים את נפשם בשדה הקרב למענה**.
    ולפיכך יש לברך על ההחלטה לביטול הפרס בשנה זו.
    ###

    סיכום:
    **עמית סגל - סיכום יומי | 18-03-2024**

    **חדשות**
    - צה״ל פועל בבית החולים שיפא בעזה בעקבות מידע על בכירי חמאס הפועלים שם. במהלך הלילה התנהלו חילופי אש במקום ונכון לשעה זו נעצרו 80 איש.
    - בוצעה תקיפה ממוקדת בה נהרג ראש מנהלת המבצעים בבטחון הפנים של חמאס.
    - במסגרת הפעולה בשיפא חוסלו כ-20 מחבלים ונעצרו עשרות.
    - אותרו אמל"ח רב וכספי טרור בבית החולים.
    - המשלחת האמריקאית דיווחה על חיסולו של מרוואן עיסא.
    - ישראל תשלח משלחת מדינית לוושינגטון להסביר את כוונותיה באשר לרפיח.
    - פרס ישראל לרב יצחק יוסף בוטל בהחלטתו.

    **פרשנויות**
    - הסיעות "ימין ממלכתי" ו"מחנה ממלכתי" הטילו וטו על הצעת חוק שירותי הדת היהודיים, ככל הנראה כתגובת מחיר להתנגדות דרעי להצעת חוק גיוס.
    - הנשיא הרצוג הביע אמון בצה״ל ובמפקדיו.
    - לפיד דרש בישיבת סיעתו להסיר את גנץ ואייזנקוט מהממשלה, בטענה שהם מעניקים לגיטימציה לליכוד.
    - נתניהו הדגיש את החשיבות של סיוע הומניטרי לרצועה כהכרחי להחלשת חמאס.
    ***

    ההודעות:
    ###
    '''

    for message in messages[::-1]:
        prompt_text += message.text + '\n' + '###' + '\n'
    print(prompt_text)

    response = model.generate_content(prompt_text)
    
    return response.text + 2*'\n' + summary_end

async def send_summary(client, destination_channel_id, summarized_message):
    # Send the summarized message to the destination channel
    await client.send_message(destination_channel_id, summarized_message)

async def main():
    # Initiate relevant consts with appropriate values
    api_id = os.environ.get('TELEGRAM_API_ID')
    api_hash = os.environ.get('TELEGRAM_API_HASH')

    # Create a TelegramClient instance
    client = TelegramClient('mysession', api_id, api_hash)
    await client.start(os.environ.get('PHONE_NUMBER'))

    '''
    # To find the chatID for the first time, replace 'your_channel_name' with the name of the source channel and run this lines:
    source_channel_name = "🇮🇱 עמית סגל - סיכום יומי 🇮🇱"
    source_channel_id = await get_channel_id(client, source_channel_name)
    print("Source Channel ID:", source_channel_id)
    '''

    # Define source and destination's channel id's
    source_channel_id = SRC_CHANNEL_ID
    destination_channel_id = DST_CHANNEL_ID

    # Get all messages sent today from the source channel
    messages = await get_todays_messages(client, source_channel_id)
    
    # Summarize the messages
    summarized_message = await summarize(messages)
    print(summarized_message)

    # Send the summarized message to the destination channel
    await send_summary(client, destination_channel_id, summarized_message)

    # Remember to stop the client
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
