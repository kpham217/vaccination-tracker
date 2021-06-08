import get_data
import process_data
import os

if __name__ == "__main__":
    # vaxsites_filepath = 'F:/PycharmProjects/vaccination-tracker/scraping-script/population density data/Halifax.csv'
    data_link = 'https://sync-cf2-1.canimmunize.ca/fhir/v1/public/booking-page/17430812-2095-4a35-a523-bb5ce45d60f1/appointment-types?forceUseCurrentAppointment=false&preview=false'
    bookingTime_link = ['https://sync-cf2-1.canimmunize.ca/fhir/v1/public/availability/17430812-2095-4a35-a523-bb5ce45d60f1?appointmentTypeId=', '&timezone=America%2FHalifax&preview=false']

    # assign path
    path, dirs, files = next(os.walk("./scraping-script/population density data/"))
    file_count = len(files)
    array = [[] for _ in range(file_count)]

    # append datasets to the list
    for i in range(file_count):
        print(">>> Processing Region " + str(i))
        vaxsites_filepath = "./scraping-script/population density data/" + files[i]
        ref_list = get_data.get_ref_data(vaxsites_filepath)
        updated_list = get_data.get_updated_data(data_link)
        broadcast_list = process_data.processing(ref_list, updated_list, bookingTime_link)
        array[i] = broadcast_list

    print(array)


