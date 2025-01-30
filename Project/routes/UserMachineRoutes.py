
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from services.MachineService import MachineService
from services.UserMachineService import UserMachineService
from services.ResultService import ResultService
from flask import render_template
import logging
from models.users import User
from io import BytesIO
from reportlab.pdfgen import canvas


logger = logging.getLogger(__name__)
user_machine_bp = Blueprint('userMachine', __name__)

@user_machine_bp.route('/api/deleteMachines', methods=['GET'])
def getAdminMachines():
    
    logger.debug("Get machines endpoint called")
    
    machines = MachineService.get_all_machines()
    machine_dicts = [m.to_dict() for m in machines]
    
    return jsonify(machine_dicts),200



@user_machine_bp.route('/api/getUserMachines', methods=['GET'])
def getMachines():
    
    logger.debug("Get machines endpoint called")
    
    current_user_id = session.get('user_id')
    
    print("GET USER MACHINES User_ID", current_user_id)
    # if not current_user_id:
    #     return jsonify({'status': 401, 'message': 'Unauthorized access'}), 401
    machines = UserMachineService.get_user_machines(current_user_id)
    print("using getUserMachines API ", machines)
    logger.debug("Debugged machines", machines)
    
    return jsonify(machines), 200



@user_machine_bp.route('/delinkMachine/<int:machine_id>', methods=['POST'])
def delinkMachine(machine_id):
    logger.debug("Delink machine endpoint called")
    logger.debug(f"Delink machine endpoint called for machine_id: {machine_id}")

    if request.method == 'POST':
        user_id = session.get('user_id')
        try:
            logger.debug("Delink machine")
            logger.debug("Machine Code is", machine_id)
            response = UserMachineService.delink_machine(machine_id,user_id)
            if response == 404:
                flash("Machine not found", "error")
                return jsonify({"error": "Machine not found"}), 404
            else:
                return render_template('dashboard.html')
        except ValueError as e:
            flash(str(e), "error")
            return jsonify({"error": str(e)}), 400
    return redirect('/dashboard')


@user_machine_bp.route('/linkMachine', methods=['GET','POST'])
def linkMachine():  
    logger.debug("Add machine endpoint called")
    if request.method == 'GET':
        return render_template('dashboard.html')
    if request.method == 'POST':
        # machine_code = request.form.get('machine_code')
        # current_user_id = session.get('user_id')
        # machine_password = request.form.get('machine_password')
        data = request.get_json()
        current_user_id = data.get('user_id')
        machine_code = data.get('machine_code')
        machine_password = data.get('machine_password')
        if not current_user_id:
            flash("Please log in first.", "error")
            return redirect('/login')
        try:
            logger.debug("Register machine")
            logger.debug("Machine Code is", machine_code)
            response = MachineService.find_machine_and_link(machine_code, machine_password, current_user_id)
            if response == 404:
                flash("Machine not found", "error")
                return jsonify({"error": "Machine not found"}), 404
            elif response == 403:
                flash("Invalid Machine Password", "error")
                return jsonify({"error": "Invalid Machine Password"}), 403
            elif response == 401:
                return jsonify({"error": "Machine has been deleted"}), 401
            else:
                return redirect('/dashboard')
        except ValueError as e:
            flash(str(e), "error")
            return jsonify({"error": str(e)}), 400
    return redirect('/dashboard')

