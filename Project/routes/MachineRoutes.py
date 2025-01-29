from flask import Blueprint, render_template, request, redirect, flash, session,jsonify,Flask
from services.MachineService import MachineService
from flask import render_template
import boto3
import logging
import os
logger = logging.getLogger(__name__)
machine_bp = Blueprint('machine', __name__)

@machine_bp.route('/admin/delete', methods=['GET','POST'])
def admin_delete():
    machine_id = request.args.get('machine_id')
    print('Machine_ID: ',machine_id)
    machine = MachineService.machine_verification(machine_id)
    print('HEre is my Machine',machine)
    is_deleted = MachineService.delete_machine(machine)
    if is_deleted:
        return jsonify({'status': 'success', 'status_code': 200})
    else:
        return jsonify({'status': 'failed', 'status_code': 400})

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


@machine_bp.route('/admin/create', methods=['GET','POST'])
def adminCreate():
    logger.debug("Add machine endpoint called")
    if request.method == 'GET':
        return render_template('dashboard.html')
    
    data = request.get_json()  
    machine_name = data.get('machine_name')
    machine_code = data.get('machine_code')
    machine_password = data.get('machine_secret')
    machine_description = data.get('machine_desc')
    machine_profile_img = data.get('img_icon')
    current_user_id = data.get('user_id')

    if not current_user_id:
        flash("Please log in first.", "error")
        return redirect('/login')
    
    try:
        logger.debug("Register machine")
        
        if request.method == "POST":
            
            MachineService.register_machine(current_user_id,machine_name,machine_password,machine_code,machine_description,machine_profile_img)
            flash("Machine added successfully!", "success")
            return jsonify({'status': 'success', 'status_code': 200})
        elif request.method == "PUT":
            MachineService.update_admin_machine(machine_name,machine_password,machine_code,machine_description,machine_profile_img)
    except ValueError as e:
        flash(str(e), "error")
        return jsonify({'status': 'failed', 'status_code': 400})

    return redirect('/dashboard')

@machine_bp.route('/api/updateMachine', methods=['GET','POST'])
def updateMachine():
    logger.debug("Update machine endpoint called")
    if request.method == 'GET':
        return render_template('dashboard.html')
    machine_code = request.form.get('machine_code')
    updated_by = request.form.get('updated_by')
    current_user_id = session.get('user_id')
    machine_id = request.args.get('machine_id')

    if not current_user_id:
        flash("Please log in first.", "error")
        return redirect('/login')
    try:
        logger.debug("Update machine")

        MachineService.update_machine(machine_code,updated_by, machine_id)
        flash("Machine updated successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect('/dashboard')