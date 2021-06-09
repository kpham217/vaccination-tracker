import os
import threading
import site_selection
import twitter_bot


if __name__ == "__main__":
    # vaxsites_filepath = 'F:/PycharmProjects/vaccination-tracker/scraping-script/population density data/Halifax.csv'
    data_link = 'https://sync-cf2-1.canimmunize.ca/fhir/v1/public/booking-page/17430812-2095-4a35-a523-bb5ce45d60f1/appointment-types?forceUseCurrentAppointment=false&preview=false'
    booking_time_link = ['https://sync-cf2-1.canimmunize.ca/fhir/v1/public/availability/17430812-2095-4a35-a523-bb5ce45d60f1?appointmentTypeId=', '&timezone=America%2FHalifax&preview=false']

    # assign path
    path, dirs, files = next(os.walk("./scraping-script/population density data/"))
    file_count = len(files)
    array = [[] for _ in range(file_count)]

    try:
        th1 = threading.Thread(target=site_selection.selection, args=(array, files, file_count, data_link, booking_time_link))
        th1.start()
        th2 = threading.Thread(target=twitter_bot.create_bot, args=(array, file_count))
        th2.start()

    except:
        print("Error: unable to start thread")




