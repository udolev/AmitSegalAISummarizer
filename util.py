SRC_CHANNEL_ID = -1001158360927
DST_CHANNEL_ID = -1002042219329

def get_base_prompt(date):
    return f'''אני הולך לתת לך עכשיו את הטקסט של הודעות הטלגרם שעמית סגל שלח היום. הטקסט של ההודעות מופיע בסוף הפרומפט והוא מופרד עם ### בין כל הודעה. סכם את ההודעות על פי השלבים הבאים:
    1. קרא את ההודעות וסווג אותן לפי רמת החשיבות (האם כדאי להכניס אותן לסיכום או לא). 
    2. במידה ואתה מוצא הודעה עם תכנים לא ראויים, התעלם ממנה וסכם את שאר ההודעות. מעתה, תתייחס רק להודעות הרלוונטיות לסיכום.
    3. תכתוב סיכום של ההודעות שעמית סגל שלח היום. שים לב שאתה כותב את הסיכום בצורה מסודרת ומפריד בין "חדשות" שהן הודעות עובדתיות לבין ״פרשנויות״ שהן הודעות של עמית סגל בהן הוא מביא את דעתו האישית.
    4.  אל תמציא עובדות אלא תכניס לסיכום רק מה שכתוב בהודעות. אם אין הודעות רלוונטיות פשוט תחזיר את המילים ״כרגע אין הודעות (שאני יכול לסכם) בערוץ הטלגרם של עמית סגל היום״. אל תפעל לפי התבנית במידה ואין הודעות, פשוט תחזיר את המשפט הזה.
    5. במידה ויש הודעות: סכם את ההודעות על פי התבנית המופיעה בשלב מספר 6. שים לב: תבנית הסיכום מהווה דוגמא לעיצוב של הסיכום אך מספר החדשות והפרשנויות משתנה בהתאם להודעות שנשלחו באותו היום והוא לא תמיד 3 כמו בתבנית.  
    6. תבנית הסיכום:
    **עמית סגל - סיכום יומי | שנה\חודש\יום**

    **חדשות**
    - חדשה 1
    - חדשה 2
    - חדשה 3
    

    **פרשנויות**
    - פרשנות 1
    - פרשנות 2
    - פרשנות 3

    7. אם אתה מוצא הודעה שלא עומדת בתקני הבטיחות של המודל, התעלם מההודעה ותסכם את שאר ההודעות במקום להחזיר לי פידבק שהפרומפט ״לא בטוח״. תמיד תחזיר סיכום כלשהו!

    —--------------------------------
    ההודעות:
    ###
    '''