from flask import Blueprint, render_template, request, redirect, flash, session,jsonify,Flask
from services.MachineService import MachineService
from flask import render_template
import boto3
import logging
import os
logger = logging.getLogger(__name__)
machine_bp = Blueprint('machine', __name__)

@machine_bp.route('/admin/delete/<int:id>', methods=['DELETE'])
def admin_delete(id):
    if request.method == "DELETE":
        
        user_id = session.get('user_id')
       
        print('Machine_ID: ',id)
        machine = MachineService.machine_verification(id,user_id)
        
        print('Here is my Machine',machine)
        is_deleted = MachineService.delete_machine(machine)
        if is_deleted:
            return jsonify({'status': 200, 'message' : 'Machine Deleted Successfully'}),200
        else:
            return jsonify({'status': 400, 'message' : 'Machine deletion failed'}),400

@machine_bp.route('/uploadFile', methods=['POST'])
def uploadFile():
	attachment_file = request.files.get("file_doc")
	if attachment_file is not None:
		filename = attachment_file.filename
		s3_object_key = f'instagram/{filename}'
		
		s3 = boto3.client('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
		try:
			s3.upload_fileobj(Fileobj=attachment_file,Bucket=os.environ.get('S3_BUCKET_NAME'),Key=s3_object_key)
			image_url=f'https://dl5hm3xr9o0pk.cloudfront.net/instagram/{filename}'
			print(f"Successfully uploaded {image_url} to {os.environ.get('S3_ACCESS_KEY')}/{s3_object_key}")
			s3.close()
			return jsonify({'filename': filename, 'file_base64': image_url})
		except FileNotFoundError:
			print(f"The file {image_url} was not found.")
			return jsonify(400)

@machine_bp.route('/admin/get/<int:machine_id>', methods=['GET'])
def adminGetID(machine_id):
    logger.debug("Get machine by ID endpoint called")
    logger.debug(f"Request Args: {request.view_args}")
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect('/login')
    
    machine = MachineService.get_by_ID(machine_id,user_id)
    if machine:
        return jsonify(machine.to_dict()),200
    else:
        return jsonify({'status': 400, 'message' : 'Machine not found'}),400
    
@machine_bp.route('/admin/get/all', methods=['GET'])
def adminGetAll():
    current_user_id = session.get('user_id')
    if not current_user_id:
        flash("Please log in first.", "error")
        return redirect('/login')
    logger.debug("Get machines endpoint called")
    machines = MachineService.get_all_machines(created_by=current_user_id)
    print("Machinesssssss",machines)
    machine_dicts = [   
        {
            "id": m[0],
            "machine_name": m[1],
            "machine_code": m[2],
            "machine_password": m[3],
            "created_by": m[4]
        }
        for m in machines
    ]
    return jsonify(machine_dicts),200

@machine_bp.route('/admin/create', methods=['POST','PUT'])
def adminCreate():
    logger.debug("Add machine endpoint called")
    
    data = request.get_json()  
    machine_name = data.get('machine_name')
    machine_code = data.get('machine_code')
    machine_password = data.get('machine_secret')
    machine_description = data.get('machine_desc')
    machine_profile_img = data.get('img_icon')
    
    current_user_id = session.get('user_id')
    if not current_user_id:
        flash("Please log in first.", "error")
        return redirect('/login')
    try:
        logger.debug("Register machine")
        if request.method == "POST":
            MachineService.register_machine(current_user_id,machine_name,machine_password,machine_code,machine_description,machine_profile_img)
            flash("Machine added successfully!", "success")
            return jsonify({'status': 200, 'message' : 'Machine added Successfully'}),200
        
        elif request.method == "PUT":
            machine_id=data.get('id')
            print(machine_id,machine_profile_img)
            MachineService.update_admin_machine(machine_id,current_user_id,machine_name,machine_password,machine_code,machine_description,machine_profile_img)
            return jsonify({'status': 200, 'message' : 'Machine update Successfully'}),200
    except ValueError as e:
        flash(str(e), "error")
        return jsonify({'status': 400, 'message' : 'Machine Deletion Failed'}),400
    return redirect('/dashboard')
