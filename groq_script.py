from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import pymysql
import logging

def get_viral(cur):
    try: 
        cur.execute("SELECT `Description` FROM `viral_videos`;")
        existing_videos = {row[0] for row in cur.fetchall()}
        return existing_videos
    except Exception as e:
        print(f"Error fetching top videos: {e}")
        return []

def get_top_video(cur):
    try:
        cur.execute("""
            SELECT `Description`
            FROM `videos`
            ORDER BY `views` DESC
            LIMIT 5;
        """)
        top_videos = [row[0] for row in cur.fetchall()]
        return top_videos
    except Exception as e:
        print(f"Error fetching top videos: {e}")
        return []


def mysqlconnect():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password="",
            db='project_social_media_spil',
        )
        with connection.cursor() as cur:
            topic = "Anda adalah seorang content creator expert"
            viral_video = get_viral(cur=cur)
            top_video = get_top_video(cur=cur)
            if viral_video:
                llm = ChatGroq(
                    model='llama-3.3-70b-versatile',
                    api_key="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"
                )

                prompt_template = f'''
                Berikut ini merupakan deskripsi top video dari akun ptspil: {top_video}.
                Berikut ini merupakan topik 10 video yang sekarang sedang viral: {{{viral_video}}}.
                {topic}, Buatlah 5 ide baru yang akan diupload di akun tiktok ptspil dengan menerapkan trend/topik yang ada dari 10 video yang sedang viral. 
                Output berupa:
                1. script narator/percakapan dan adegannya , Saran efek atau transisi yang populer (paragraf)
                2. deskripsi/caption yang menarik (paragraf)
                3. Saran durasi video (1 kalimat)
                4. Berikan judul musik yang paling sering digunakan pada suatu topik yang sedang viral (1 kalimat dengan nama artis)
                
                '''


                prompt = ChatPromptTemplate.from_template(
                    template = prompt_template
                )
                    

                # Create and run the chain
                chain = prompt | llm
                    
                # Get the response
                response = chain.invoke({"text": topic})

                print(response.content)
                connection.commit()
            else:
                logging.warning("No viral videos found.")
    except Exception as e:
        logging.error(f"Database connection error: {e}")

if __name__ == "__main__":
    mysqlconnect()