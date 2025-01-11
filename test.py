def insert_videos(cur, videos):
    try:
        # Ambil semua link yang sudah ada di database
        cur.execute("SELECT `id`, `link` FROM `videos`;")
        existing_videos = {row[1]: row[0] for row in cur.fetchall()}  # {link: id}
        print("oke1")
        
        # Pisahkan video baru dan video yang perlu diupdate
        videos_to_update = [video for video in videos if video['link'] in existing_videos]
        videos_to_insert = [video for video in videos if video['link'] not in existing_videos]
        
        # Update video yang sudah ada di database
        if videos_to_update:
            update_query = """
                UPDATE `videos` 
                SET `Views` = %s
                WHERE `id` = %s;
            """
            data_to_update = [
                (video['views'], existing_videos[video['link']]) 
                for video in videos_to_update
            ]
            cur.executemany(update_query, data_to_update)
            print(f"{len(videos_to_update)} video berhasil diupdate.")
        
        # Insert video baru ke database
        if videos_to_insert:
            insert_query = """
                INSERT INTO `videos` (`Views`, `link`, `Description`)
                VALUES (%s, %s, %s);
            """
            data_to_insert = [
                (video['views'], video['link'], video['description']) 
                for video in videos_to_insert
            ]
            cur.executemany(insert_query, data_to_insert)
            print(f"{len(videos_to_insert)} video baru berhasil diinsert ke database.")
        
        if not videos_to_insert and not videos_to_update:
            print("Tidak ada perubahan pada database.")

    except Exception as e:
        print(f"Error saat menginsert atau mengupdate video: {e}")
