from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

import os
llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    api_key="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"
)
# pick random topic
topic = "Berikut top 5 video tiktok teratas dari akun ptspil(views, description):1. 290000, Siapa yang rumahnya dekat kantor tapi sering telat? Coba tonton video ini dulu. Amri setiap hari berangkat kerja jam 4 pagi, pulang pergi Mojokerto Surabaya. Jadi telat ke kantor itu bukan jadi alasan ya guys, kalau bisa manage waktu dengan baik. #vlog #adayinmylife  dibuat oleh What’s on SPIL ? dengan original sound - What’s on SPIL ? karya What’s on SPIL ?2. 184200, Gimana sih kehidupan seorang fresh graduate di Surabaya? Kenalin Nia, setelah lulus kuliah dia langsung diterima di PT SPIL sebagai seorang Customer Service. Sehari-hari, Nia bertugas untuk memastikan ketersediaan kontainer terakomodasi dan terkirim sesuai jadwal. #vlog #adayinmylife  dibuat oleh What’s on SPIL ? dengan original sound - What’s on SPIL ? karya What’s on SPIL ?3. 114600, Crew Kapal SPIL Luzon sedang standby. Mereka keren ya guys mirip adegan di film action👨🏻‍✈️🚢⚓️ #fyp #foryou #trending  dibuat oleh What’s on SPIL ? dengan original sound - What’s on SPIL ? karya What’s on SPIL ?4. 106400, Hi guys, sudah tahu belum istilah untuk orang-orang (crew) yang bekerja di bagian mesin kapal? 1. Kepala Mesin (Chief Engineer): Kepala Mesin adalah orang yang bertanggung jawab penuh atas operasional dan kinerja sistem mesin kapal. Mereka mengawasi dan mengkoordinasikan pekerjaan seluruh departemen mesin kapal. 2. Perwira Mesin (Engine Officer): Perwira Mesin bertanggung jawab langsung atas operasional dan pemeliharaan mesin kapal. Mereka mengawasi sistem mesin, mengkoordinasikan perawatan rutin, dan memastikan semua peralatan berfungsi dengan baik. 3. Operator Mesin (Engine Operator): Operator Mesin bertanggung jawab menjalankan dan mengoperasikan sistem mesin kapal. Mereka memastikan pengoperasian yang aman dan efisien dari mesin utama, generator listrik, sistem bahan bakar, sistem pendingin, dan sistem lainnya. 4. Teknisi Mesin (Engine Technician): Teknisi Mesin melakukan perawatan rutin, perbaikan, dan inspeksi sistem mesin kapal. Mereka memiliki pengetahuan mendalam tentang mesin dan sistem mekanis, serta dapat melakukan pemeliharaan preventif dan perbaikan saat terjadi kerusakan. 5. Montir Mesin (Engine Fitter): Montir Mesin bertanggung jawab untuk memasang, merakit, dan memperbaiki bagian-bagian mesin kapal. Mereka membantu dalam perbaikan rutin dan pemeliharaan mesin, serta dapat melakukan penggantian komponen yang rusak. 6. Ahli Mesin (Marine Engineer): Ahli Mesin adalah orang yang memiliki pengetahuan mendalam tentang prinsip-prinsip mesin dan sistem mekanis kapal. Mereka terlibat dalam desain, pengembangan, dan pengujian sistem mesin baru, serta memberikan saran teknis untuk perbaikan dan peningkatan kinerja. Ada yang terlewat dari mimin kah? 🤔 #fyp #foryou #trending  dibuat oleh What’s on SPIL ? dengan DJ SAH - Tiktok karya Sarah Suhairi5.  93600, Kapal SPIL Kartini sebelum terisi muatan, perbedaan pagi dan malam hari 🚢⚓️ - Airnya biru banget ya mimin jadi ingin main air 🥰 #fyp #foryou #trending  dibuat oleh What’s on SPIL ? dengan Hero karya Alan Walker & Sasha Alex Sloan. Berikut top 5 ide viral di tiktok: 1. Description: (Added January 7, 2025) “That Don’t Impress Me Much” Trend | Example:Link: https://vm.tiktok.com/ZNeKXjkKv/2. Description: (Added January 5, 2025) “Oh It’s Useless to Yell” Trend | Example: Link: https://vm.tiktok.com/ZNeKFknnn/ 3. Description: (Added January 1st, 2025) Ideal Future Trend| Example:  Link: https://vm.tiktok.com/ZNewW5EWA/ 4. Description: (Added December 30th, 2024) Link: https://vm.tiktok.com/ZNewWDgcx/5. Description: (Added December 28th, 2024) “Are You Kidding? That’s Unfair” Trend | Example: Link: https://vm.tiktok.com/ZNewQ8N1B/"

prompt_template = f'''
{topic}Buatlah 5 ide baru yang berkaitan dengan ptspil dengan melihat top ide yang viral. output berupa:1. script 2. deskripsi/caption
'''

prompt = ChatPromptTemplate.from_template(
    template = prompt_template
)
    

# Create and run the chain
chain = prompt | llm
    
# Get the response
response = chain.invoke({"text": topic})

print(response.content)