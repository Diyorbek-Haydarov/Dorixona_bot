#!/usr/bin/env python3
"""
Sample data population script
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.database import db

async def add_sample_data():
    """Add sample medicines and first aid articles"""
    print("📊 PharmaGuide Bot - Sample Data Setup")
    print("=====================================")
    print()
    
    # Initialize database
    await db.init_db()
    print("✅ Database initialized")
    
    # Sample medicines
    sample_medicines = [
        {
            'name_latin': 'Paracetamol',
            'name_cyrillic': 'Парацетамол',
            'description_latin': 'Og\'riq qoldiruvchi va isitma pasaytiruvchi dori',
            'description_cyrillic': 'Оғриқ қолдирувчи ва иситма пасайтирувчи дори',
            'composition_latin': 'Paracetamol 500mg',
            'composition_cyrillic': 'Парацетамол 500мг',
            'usage_latin': 'Kattalar: 1-2 tablet, kuniga 3-4 marta. Bolalar uchun yoshiga qarab',
            'usage_cyrillic': 'Катталар: 1-2 таблетка, кунига 3-4 марта. Болалар учун ёшига қараб',
            'side_effects_latin': 'Jigar shikastlanishi, allergik reaktsiya',
            'side_effects_cyrillic': 'Жигар шикастланиши, аллергик реакция',
            'voice_file_id': ''
        },
        {
            'name_latin': 'Ibuprofen',
            'name_cyrillic': 'Ибупрофен',
            'description_latin': 'Yallig\'lanishga qarshi va og\'riq qoldiruvchi dori',
            'description_cyrillic': 'Яллиғланишга қарши ва оғриқ қолдирувчи дори',
            'composition_latin': 'Ibuprofen 400mg',
            'composition_cyrillic': 'Ибупрофен 400мг',
            'usage_latin': 'Kattalar: 1 tablet, kuniga 3 marta. Ovqat bilan birga',
            'usage_cyrillic': 'Катталар: 1 таблетка, кунига 3 марта. Овқат билан бирга',
            'side_effects_latin': 'Oshqozon shikastlanishi, bosh og\'rig\'i',
            'side_effects_cyrillic': 'Ошқозон шикастланиши, бош оғриғи',
            'voice_file_id': ''
        },
        {
            'name_latin': 'Aspirin',
            'name_cyrillic': 'Аспирин',
            'description_latin': 'Og\'riq qoldiruvchi, isitma pasaytiruvchi va qon suyuqlashtiruvchi',
            'description_cyrillic': 'Оғриқ қолдирувчи, иситма пасайтирувчи ва қон суюқлаштирувчи',
            'composition_latin': 'Acetylsalicylic acid 500mg',
            'composition_cyrillic': 'Ацетилсалицил кислота 500мг',
            'usage_latin': 'Kattalar: 1-2 tablet, kuniga 3 marta. Ovqat bilan birga',
            'usage_cyrillic': 'Катталар: 1-2 таблетка, кунига 3 марта. Овқат билан бирга',
            'side_effects_latin': 'Oshqozon shikastlanishi, qon ketishi',
            'side_effects_cyrillic': 'Ошқозон шикастланиши, қон кетиши',
            'voice_file_id': ''
        },
        {
            'name_latin': 'Amoxicillin',
            'name_cyrillic': 'Амоксициллин',
            'description_latin': 'Antibiotik - bakterial infeksiyalarga qarshi',
            'description_cyrillic': 'Антибиотик - бактериал инфекцияларга қарши',
            'composition_latin': 'Amoxicillin 500mg',
            'composition_cyrillic': 'Амоксициллин 500мг',
            'usage_latin': 'Kattalar: 1 kapsula, kuniga 3 marta. 7-10 kun davomida',
            'usage_cyrillic': 'Катталар: 1 капсула, кунига 3 марта. 7-10 кун давомида',
            'side_effects_latin': 'Diareya, ko\'krak qafasi, allergik reaktsiya',
            'side_effects_cyrillic': 'Диарея, кўкрак қафаси, аллергик реакция',
            'voice_file_id': ''
        },
        {
            'name_latin': 'Omeprazole',
            'name_cyrillic': 'Омепразол',
            'description_latin': 'Oshqozon kislotasini kamaytiradi',
            'description_cyrillic': 'Ошқозон кислотасини камайтиради',
            'composition_latin': 'Omeprazole 20mg',
            'composition_cyrillic': 'Омепразол 20мг',
            'usage_latin': 'Kattalar: 1 kapsula, kuniga 1 marta, bo\'sh oshqozonga',
            'usage_cyrillic': 'Катталар: 1 капсула, кунига 1 марта, бўш ошқозонга',
            'side_effects_latin': 'Bosh og\'rig\'i, ko\'ngil aynishi',
            'side_effects_cyrillic': 'Бош оғриғи, кўнгил айниши',
            'voice_file_id': ''
        }
    ]
    
    # Add sample medicines
    print("Adding sample medicines...")
    for medicine in sample_medicines:
        success = await db.add_medicine(medicine)
        if success:
            print(f"✅ Added: {medicine['name_latin']}")
        else:
            print(f"❌ Failed to add: {medicine['name_latin']}")
    
    # Sample first aid articles
    sample_first_aid = [
        {
            'title_latin': 'Qon ketishini to\'xtatish',
            'title_cyrillic': 'Қон кетишини тўхтатиш',
            'content_latin': '''1. Qon ketayotgan joyni toza mato bilan bosib turing
2. Agar qon ketish davom etsa, qo'shimcha mato qo'shing
3. Qon ketish joyini yuqoriga ko'taring
4. Agar qon ketish to'xtamasa, tez yordamga murojaat qiling
5. Qon ketish to'xtagach, joyni tozalang va bog'lang''',
            'content_cyrillic': '''1. Қон кетаётган жойни тоза мато билан босиб туринг
2. Агар қон кетиш давом этса, қўшимча мато қўшинг
3. Қон кетиш жойнини юқорига кўтаринг
4. Агар қон кетиш тўхтамаса, тез ёрдамга мурожаат қилинг
5. Қон кетиш тўхтагач, жойни тозаланг ва богланг''',
            'category': 'wounds'
        },
        {
            'title_latin': 'Yonish holatida birinchi yordam',
            'title_cyrillic': 'Ёниш ҳолатида биринчи ёрдам',
            'content_latin': '''1. Yonayotgan odamni xavfsiz joyga olib o'ting
2. Yonayotgan kiyimlarni olib tashlang
3. Sovuq suv bilan yuvib turing (15-20 daqiqa)
4. Yonish joyiga muz qo'ymang
5. Tez yordamga murojaat qiling
6. Yonish joyini toza mato bilan yoping''',
            'content_cyrillic': '''1. Ёнаётган одамни хафсиз жойга олиб ўтинг
2. Ёнаётган кийимларни олиб ташланг
3. Совуқ сув билан ювиб туринг (15-20 дақиқа)
4. Ёниш жойига муз қўйманг
5. Тез ёрдамга мурожаат қилинг
6. Ёниш жойнини тоза мато билан ёпинг''',
            'category': 'burns'
        },
        {
            'title_latin': 'Bo\'g\'ilish holatida yordam',
            'title_cyrillic': 'Бўғилиш ҳолатида ёрдам',
            'content_latin': '''1. Odamning orqasiga o'ting
2. Qo'llaringizni qorin bo'shlig'iga qo'ying
3. Yuqoriga va ichkariga bosib turing
4. Bu harakatni 5 marta takrorlang
5. Agar narsa chiqmasa, tez yordamga murojaat qiling
6. Odamning nafas olishini tekshiring''',
            'content_cyrillic': '''1. Одамнинг орқасига ўтинг
2. Қўлларингизни қорин бўшлиғига қўйинг
3. Юқорига ва ичкарига босиб туринг
4. Бу ҳаракатни 5 марта такрорланг
5. Агар нарса чиқмаса, тез ёрдамга мурожаат қилинг
6. Одамнинг нафас олишини текширинг''',
            'category': 'choking'
        },
        {
            'title_latin': 'Yurak xurujida birinchi yordam',
            'title_cyrillic': 'Юрак хуружида биринчи ёрдам',
            'content_latin': '''1. Odamni tekis yotqizing
2. Nafas olish va yurak urishini tekshiring
3. Agar nafas olmayotgan bo'lsa, sun'iy nafas bering
4. Agar yurak urmayotgan bo'lsa, qo'l bilan bosib turing
5. Tez yordamga murojaat qiling (103)
6. Davolash davom etguncha yordam berishni davom eting''',
            'content_cyrillic': '''1. Одамни текис ётқизинг
2. Нафас олиш ва юрак уришини текширинг
3. Агар нафас олмаяётган бўлса, сунъий нафас беринг
4. Агар юрак урмаяётган бўлса, қўл билан босиб туринг
5. Тез ёрдамга мурожаат қилинг (103)
6. Даволash давом этгунча ёрдам беришни давом этинг''',
            'category': 'heart'
        }
    ]
    
    # Add sample first aid articles
    print("\nAdding sample first aid articles...")
    for article in sample_first_aid:
        success = await db.add_first_aid_article(article)
        if success:
            print(f"✅ Added: {article['title_latin']}")
        else:
            print(f"❌ Failed to add: {article['title_latin']}")
    
    print()
    print("🎉 Sample data added successfully!")
    print("You can now test the bot with this sample data.")

if __name__ == "__main__":
    asyncio.run(add_sample_data())
