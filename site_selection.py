import get_data
import process_data
import schedule
import time


def selection(array, files, file_count, data_link, booking_time_link):
    # append datasets to the list
    for i in range(file_count):
        print(">>> Processing Region " + str(i+1))
        vaxsites_filepath = "./scraping-script/population density data/" + files[i]
        ref_list = get_data.get_ref_data(vaxsites_filepath)
        updated_list = get_data.get_updated_data(data_link)
        broadcast_list = process_data.processing(ref_list, updated_list, booking_time_link)
        array[i] = broadcast_list


# def selection(array, files, file_count, data_link, booking_time_link):
#     schedule.every(3).hours.do(run, array=array, files=files, file_count=file_count, data_link=data_link, booking_time_link=booking_time_link)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
