from flask import Flask, render_template, request, jsonify,redirect,flash
from pymongo import MongoClient
from bson import ObjectId,json_util
from flask_cors import CORS
import os
import json
from operator import itemgetter
app = Flask(__name__,static_folder='images')
CORS(app)
uri = "mongodb+srv://vongledata:1UVw7DhRKcRQJPY3@cluster0.t3ujmhu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database("Vongdata")
UPLOAD_FOLDER = 'images'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





#second look
@app.route('/houseselect')
def index3():
    return render_template('indexhouse.html')



@app.route('/add_call', methods=['GET', 'POST'])
def add_call():
    collection = db['test3']
    if request.method == 'POST':
        roll_number = request.form['rollNumber']
        full_name = request.form['fullName']
        vongster_photo = request.files['vongsterPhoto']
        current_status = request.form['currentStatus']
        email = request.form['email']
        grade = request.form['grade']
        city = request.form['city']
        school_name = request.form['schoolName']
        mobile_number = request.form['mobileNumber']
        device_status = request.form['deviceStatus']
        school_timing = request.form['schoolTiming']
        tuition_timing = request.form['tuitionTiming']
        house_name = request.form['houseName']
        likes_dislikes = request.form['likesDislikes']
        extra_curriculars = request.form['extraCurriculars']
        hobbies = request.form['hobbies']
        exam_schedules = request.form['examSchedules']
        last_event_attended = request.form['lastEvent']
        reasons_not_participating = request.form['reasonsForNotParticipating']
        future_participation = request.form['expectedFutureParticipation']
        preferred_timing_days = request.form['preferredTimingDays']
        reason_not_participating = request.form['reasonForNotParticipating']
        feedback = request.form['feedback']
        if vongster_photo and vongster_photo.filename != '':
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], vongster_photo.filename)
            vongster_photo.save(image_filename)
 
       
        data_to_insert = {
           'roll_number': roll_number,
            'full_name': full_name,
            'vongster_photo': vongster_photo.filename,
            'current_status': current_status,
            'email': email,
            'grade': grade,
            'city': city,
            'school_name': school_name,
            'mobile_number': mobile_number,
            'device_status': device_status,
    'school_timing': school_timing,
    'tuition_timing': tuition_timing,
    'house_name': house_name,
    'likes_dislikes': likes_dislikes,
    'extra_curriculars': extra_curriculars,
    'hobbies': hobbies,
    'exam_schedules': exam_schedules,
    'last_event_attended': last_event_attended,
    'reasons_not_participating': reasons_not_participating,
    'future_participation': future_participation,
    'preferred_timing_days': preferred_timing_days,
    'reason_not_participating': reason_not_participating,
    'feedback': feedback
        }
        collection.insert_one(data_to_insert)
        call=full_name+"_call"
        activity=full_name+"_act"
        db.create_collection(call)
        db.create_collection(activity)
        
        return redirect('/')

    return render_template('form2.html')



@app.route('/table_data')
def table():
    collection = db['test3']
    documents = collection.find({})
    full_name = request.args.get('full_name', 'Unknown')
    names = [document.get('full_name', 'Unknown') for document in documents]

    return render_template('dropdown copy.html', names=full_name)

   
#this for entering data into table of call statues

@app.route('/table_full_data_entry', methods=['GET', 'POST'])
def add_data():
    
    
    if request.method == 'POST':
        # Get data from the form
        dbname = request.form['names']
        dbname=dbname+"_call"
        collection = db[dbname]
        field1 = request.form['date']
        field2 =  request.form['Preference for Activities']
        field3 =  request.form['Preferred Time and days for Activities']
        field4 =  request.form['Reasons for Not participating']
        field5 =  request.form['Suggestions / Feedback about vong Activities']
        field6 =  request.form['Willing to participate in future (Yes / No)']
        field7 =  request.form['Upcoming /Ongoing Exam Schedule']
        # Insert data into the collection
        data_to_insert = {
            'date': field1,
            'Preference for Activities':field2,
            'Preferred Time and days for Activities': field3,
            'Reasons for Not participating':field4,
            'Suggestions / Feedback about vong Activities':field5,
            'Willing to participate in future (Yes / No)':field6,
            'Upcoming /Ongoing Exam Schedule':field7

            # Add more fields if necessary
        }
        collection.insert_one(data_to_insert)

        return redirect('/')


#Activity status table entry ,select dropdown

@app.route('/table_data_activity')
def table_data_activity():
    collection = db['test3']
    documents = collection.find({})
    names = [document.get('full_name', 'Unknown') for document in documents]

    return render_template('dropdown copy 2.html', names=names)

  

@app.route('/table_full_data_entry_activity', methods=['GET', 'POST'])
def table_full_data_entry_activity():
    dbname = request.form['selectedName']
    dbname=dbname+"_act"
    collection = db[dbname]
    if request.method == 'POST':
        # Get data from the form
        field1 = request.form['date']
        field2 =  request.form['fullName']
        # Insert data into the collection
        data_to_insert = {
            field1: field2

            # Add more fields if necessary
        }
        collection.insert_one(data_to_insert)

        return redirect('/')

#This is for show data for indivitual

@app.route('/')
def index():
    collection = db['test3']
    documents1 = collection.find({})
    documents2 = collection.find({})
    documents3 = collection.find({})
    documents4 = collection.find({})
    documents5 = collection.find({})
    documents6 = collection.find({})


    names = [document.get('full_name', 'Unknown') for document in documents1]
    firstnames = [document.get('firstname', 'Unknown') for document in documents5]
    lastnames = [document.get('lastname', 'Unknown') for document in documents6]
    schools = [document.get('institution', 'Unknown') for document in documents2]
    city = [document.get('grade', 'Unknown') for document in documents3]
    house = [document.get('house', 'Unknown') for document in documents4]
    unique_list = [item for index, item in enumerate(house) if item not in house[:index]]
    min_length = min(len(names), len(schools), len(city),len(house))
    print(unique_list)
    last_dates_list = []
    for i in names:
        collection = db[i+'_call']
        documents = collection.find({})
        dates = [document.get('date', 'Unknown') for document in documents]
        
        if dates:
            print(dates[-1])
            last_dates_list.append(dates[-1])
        else:
            last_dates_list.append(None)
    data = list(zip(names[:min_length], schools[:min_length], city[:min_length],house[:min_length],firstnames[:min_length],lastnames[:min_length],last_dates_list[:min_length]))

    return render_template('dropdown.html', data=data,house=unique_list)





# @app.route('/get_data', methods=['POST'])
# def get_data():
#     dbname = request.form['selectedName']
#     dbname=dbname+"_call"
#     collection = db[dbname]
#     cursor = collection.find({})
#     data = []
#     for document in cursor:
#         document_data = {}
#         for key, value in document.items():
#             document_data[key] = value
#         data.append(document_data)
#     dbname = request.form['selectedName']
    
#     dbname = request.form['selectedName']
#     dbname = "test3"
#     collection = db[dbname]
#     if request.method == 'POST':
#         full_name = request.form['selectedName']
#         result_cursor = collection.find({'full_name': full_name})
#         cvdata = list(result_cursor)
#     for document_data in cvdata:
#         if 'roll_number' in document_data:
#             rollnum=document_data['roll_number']
    
#     collection = db[rollnum]
#     cursor = collection.find({})
#     datac = []
#     for document in cursor:
#         document_data = {}
#         for key, value in document.items():
#             document_data[key] = value
#         datac.append(document_data)
#     return render_template('result.html', data=data, cv=cvdata,dataroll=datac)
 
@app.route('/get_data', methods=['POST'])
def get_data():
    # Get data from the first collection
    dbname = request.form['selectedName']
    dbname_call = dbname + "_call"
    collection = db[dbname_call]
    cursor = collection.find({})
    data = []
    for document in cursor:
        document_data = {}
        for key, value in document.items():
            document_data[key] = value
        data.append(document_data)

    # Get data from the second collection
    dbname = "test3"
    collection = db[dbname]
    if request.method == 'POST':
        full_name = request.form['selectedName']
        result_cursor = collection.find({'full_name': full_name})
        cvdata = list(result_cursor)
        for document_data in cvdata:
            if 'roll_number' in document_data:
                rollnum = document_data['roll_number']
        collection = db[str(rollnum)]
        cursor = collection.find({})
        cursor2 = collection.find({})
        datac = []
        datadate = []
        marks_by_date = {}
        for document in cursor:
            for key, value in document.items():
                if(key=='mark'):
                    datac.append(value)
                if(key=='date'):
                    datadate.append(value)
                    date=value
            print( document['date']) 
                   
        print(marks_by_date)

        for date, total_marks in marks_by_date.items():
            print(f"Total marks for {date}: {total_marks}")
        dataapp = []
        for document in cursor2:
            document_data = {}
            for key, value in document.items():
                document_data[key] = value
            dataapp.append(document_data)
        print(dataapp)
        return render_template('result.html', data=data, cv=cvdata, dataroll=datac, dataroll_json=json.dumps(datac),dataofpart=dataapp,datadate=datadate, datadate_json=json.dumps(datadate))


#update the vongster data

@app.route('/update')
def update():
    collection = db['test3']
    # Fetch all documents from the collection
    documents = collection.find({})
    # Extract 'full_name' from each document, provide 'Unknown' as default value if missing
    names = [document.get('full_name', 'Unknown') for document in documents]
    return render_template('update_form.html', names=names)


@app.route('/update_data', methods=['POST','GET'])
def update_data():
    
    collection = db['test3']
    
    # Retrieve data based on the selected name's roll number
    full_name = request.form['selectedName']
    # Query the collection based on the provided roll number
    result = collection.find_one({'full_name':full_name})
    
    # if result:
    #     # Get updated data from the form
    #     updated_data = {
    #         'roll_number': request.form['rollNumber'],
    #         'full_name': request.form['fullName'],
    #         'vongster_photo': request.form['vongsterPhoto'],
    #         'current_status': request.form['currentStatus'],
    #         'email': request.form['email'],
    #         'grade': request.form['grade'],
    #         'city': request.form['city'],
    #         'school_name': request.form['schoolName'],
    #         'mobile_number': request.form['mobileNumber'],
    #         'device_status': request.form['deviceStatus'],
    #         'school_timing': request.form['schoolTiming'],
    #         'tuition_timing': request.form['tuitionTiming'],
    #         'house_name': request.form['houseName'],
    #         'likes_dislikes': request.form['likesDislikes'],
    #         'extra_curriculars': request.form['extraCurriculars'],
    #         'hobbies': request.form['hobbies'],
    #         'exam_schedules': request.form['examSchedules'],
    #         'last_event_attended': request.form['lastEvent'],
    #         'reasons_not_participating': request.form['reasonsForNotParticipating'],
    #         'future_participation': request.form['expectedFutureParticipation'],
    #         'preferred_timing_days': request.form['preferredTimingDays'],
    #         'reason_not_participating': request.form['reasonForNotParticipating'],
    #         'feedback': request.form['feedback']
    #     }

    #     # Update the document in the collection
        
        
    return render_template('update_data_form.html', names=result)
    

@app.route('/update_call', methods=['GET', 'POST'])
def update_call():
    collection = db['test3']
    if request.method == 'POST':
        # Get data from the form
        roll_number = request.form['rollNumber']
        full_name = request.form['fullName']
      
        current_status = request.form['currentStatus']
        email = request.form['email']
        grade = request.form['grade']
        city = request.form['city']
        school_name = request.form['schoolName']
        mobile_number = request.form['mobileNumber']
        device_status = request.form['deviceStatus']
        school_timing = request.form['schoolTiming']
        tuition_timing = request.form['tuitionTiming']
        house_name = request.form['houseName']
        likes_dislikes = request.form['likesDislikes']
        extra_curriculars = request.form['extraCurriculars']
        hobbies = request.form['hobbies']
        exam_schedules = request.form['examSchedules']
        last_event_attended = request.form['lastEvent']
        reasons_not_participating = request.form['reasonsForNotParticipating']
        future_participation = request.form['expectedFutureParticipation']
        preferred_timing_days = request.form['preferredTimingDays']
        reason_not_participating = request.form['reasonForNotParticipating']
        feedback = request.form['feedback']
      
 
        # Insert data into the collection
       
        data_to_insert = {
           'roll_number': roll_number,
            'full_name': full_name,
            'current_status': current_status,
            'email': email,
            'grade': grade,
            'city': city,
            'school_name': school_name,
            'mobile_number': mobile_number,
            'device_status': device_status,
    'school_timing': school_timing,
    'tuition_timing': tuition_timing,
    'house_name': house_name,
    'likes_dislikes': likes_dislikes,
    'extra_curriculars': extra_curriculars,
    'hobbies': hobbies,
    'exam_schedules': exam_schedules,
    'last_event_attended': last_event_attended,
    'reasons_not_participating': reasons_not_participating,
    'future_participation': future_participation,
    'preferred_timing_days': preferred_timing_days,
    'reason_not_participating': reason_not_participating,
    'feedback': feedback
        }
        collection.update_one({'full_name': full_name},  {'$set': data_to_insert})
        return redirect('/')
    # If it's a GET request, serve the form
def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Serialize ObjectId to its string representation
    raise TypeError("Type not serializable")



#whole data view
@app.route('/last_added_documents', methods=['GET'])
def get_last_added_documents():
    result = {}
    # Get the list of all collection names in the database
    collection_names = db.list_collection_names()

    for collection_name in collection_names:
        # Check if the collection name contains "_call"
        if '_call' in collection_name:
            # Get the last added document in the collection
            collection = db[collection_name]
            last_document = collection.find_one(sort=[('_id', -1)], projection={'_id': False})  # Exclude _id field
            if last_document:
                # Get the corresponding full name and house name from the 'test3' collection
                full_name = collection_name.replace('_call', '')
                test3_collection = db['test3']
                user_data = test3_collection.find_one({'full_name': full_name})
                if user_data and 'house' in user_data:
                    house_name = user_data['house']
    # Rest of your code
                else:
    # Handle the case where 'house_name' is not present or user_data is None
                    house_name = 'Default House Name'

                if house_name not in result:
                    result[house_name] = []
                result[house_name].append({
                    'full_name': full_name,
                    'last_document': last_document
                })

    # Sort the result dictionary by house name
    sorted_result = dict(sorted(result.items(), key=itemgetter(0)))

    return render_template('last_added_documents.html', data=sorted_result)
@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        data = request.json  # Access the JSON data sent from the client
        selected_status = data.get('status')
        full_name = data.get('fullname', 'Unknown')
        print('hello')
        print(full_name)

        collection = db['test3']
        result = collection.update_one({'full_name': full_name}, {'$set': {'active': selected_status}})

        if result.modified_count > 0:
            return jsonify({'success': True, 'message': f'Status updated successfully for {full_name}'})
        else:
            return jsonify({'success': False, 'message': f'Failed to update status for {full_name}'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500  

@app.route('/table_full_data_entry_update', methods=['GET', 'POST'])
def add_data2():
    
    roll_num = request.args.get('full_name', 'Unknown')
    if request.method == 'POST':
        # Get data from the form
        
        dbname = roll_num + "_call"
        collection = db[dbname]
        field1 = request.form['date']
        field2 = request.form['Preference for Activities']
        field3 = request.form['Preferred Time and days for Activities']
        field4 = request.form['Reasons for Not participating']
        field5 = request.form['Suggestions / Feedback about vong Activities']
        field6 = request.form['Willing to participate in future (Yes / No)']
        field7 = request.form['Upcoming /Ongoing Exam Schedule']
        
        # Define the criteria for the update
        filter_criteria = {'date': field1, 'Preference for Activities': field2, 'Preferred Time and days for Activities': field3}
        
        # Set the data to be updated or inserted
        data_to_update = {
            'date': field1,
            'Preference for Activities': field2,
            'Preferred Time and days for Activities': field3,
            'Reasons for Not participating': field4,
            'Suggestions / Feedback about vong Activities': field5,
            'Willing to participate in future (Yes / No)': field6,
            'Upcoming /Ongoing Exam Schedule': field7
        }

        # Perform the update or insert
        result = collection.update_one(filter_criteria, {'$set': data_to_update}, upsert=True)

        if result.modified_count > 0:
            # Document updated
            return redirect('/')
        elif result.upserted_id:
            # New document inserted
            return redirect('/')
        else:
            # No changes made
            return "No changes made"

    # Handle other HTTP methods (e.g., GET) as needed
    return "Invalid request method"

from flask import render_template

from flask import render_template

@app.route('/get_data_score', methods=['GET', 'POST'])
def get_data_score():
    dbname = "test3"
    collection = db[dbname]
    documents = collection.find()
    data_set = []

    for document in documents:
        if 'roll_number' in document and 'full_name' in document and 'house' in document:
            roll_number = document['roll_number']
            full_name = document['full_name']
            house = document['house']

            rollnum_collection_name = str(roll_number)
            rollnum_collection = db.get(rollnum_collection_name)  # Use get to handle potential None
            if rollnum_collection:
                rollnum_documents = rollnum_collection.find()

                total_marks = sum(document.get('mark', 0) for document in rollnum_documents)

                student_data = {
                'Roll Number': roll_number,
                'Full Name': full_name,
                'House': house,
                'Total Marks': total_marks
                }

            data_set.append(student_data)

# Print the data set
        for data in data_set:
            print(f"Roll Number: {data['Roll Number']}, Full Name: {data['Full Name']}, House: {data['House']}, Total Marks: {data['Total Marks']}")
        
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
