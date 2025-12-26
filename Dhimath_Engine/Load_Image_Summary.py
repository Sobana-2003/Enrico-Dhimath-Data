import pandas as pd 

def load_image_summary(image_summary_file_path, pdf_name):
    usecols = ["Slide_Summary", "Slide_Number",]
    summary_file_name = image_summary_file_path + f"\\{pdf_name}_Image_summary.txt"
    #print(summary_file_name)
    df = pd.read_csv(summary_file_name, usecols = usecols,delimiter="|" )
    image_summary = df.sort_values("Slide_Number")
    #image_summary = r_df.copy()
    # file = open(summary_file_name, "r")
    # image_summary = list(csv.reader(file, delimiter="|"))
    #print("Length of Image Summary: ", len(image_summary))
    return image_summary