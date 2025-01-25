def change_txt_filename_to_url(txt_filename):
    return "https://" + txt_filename.replace("_", "/").replace(".txt", "")