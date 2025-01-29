
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
user_machine_bp = Blueprint('User_machine', __name__)

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
    print("HERE WE ARE USING SESSION.GET", current_user_id)
    User = UserMachineService.get_user_machines(current_user_id)
    if not User:
        flash("Please log in first.", "error")
        logger.debug("No user logged in")
        return redirect('/login')
    
    user_machines = User.machines
    print("using getUserMachines API ", user_machines)

    
    machine_dicts = [m.to_dict() for m in user_machines]
    
    return jsonify(machine_dicts),200


@user_machine_bp.route('/delinkMachine', methods=['GET','POST'])
def delinkMachine():
    logger.debug("Delink machine endpoint called")
    if request.method == 'GET':
        return render_template('dashboard.html')
    if request.method == 'POST':
        data = request.get_json()  
        machine_id = data.get('machine_id')
        try:
            logger.debug("Delink machine")
            logger.debug("Machine Code is", machine_id)
            response = UserMachineService.find_machine_delink(machine_id)
            if response == 404:
                flash("Machine not found", "error")
                return jsonify({"error": "Machine not found"}), 404
            else:
                return jsonify({"success": "Machine found"}), 200
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
        current_user_id = session.get('user_id')
        # machine_password = request.form.get('machine_password')
        
        # if not current_user_id:
        #     flash("Please log in first.", "error")
        #     return redirect('/login')
        data = request.get_json()  
        machine_code = data.get('machine_code')
        machine_password = data.get('machine_password')
        user_id = data.get('user_id')
        try:
            logger.debug("Register machine")
            logger.debug("Machine Code is", machine_code)
            response = MachineService.find_machine_and_link(machine_code, machine_password, user_id)
            if response == 404:
                flash("Machine not found", "error")
                return jsonify({"error": "Machine not found"}), 404
            elif response == 403:
                flash("Invalid Machine Password", "error")
                return jsonify({"error": "Invalid Machine Password"}), 403
            elif response == 401:
                return jsonify({"error": "Machine has been deleted"}), 401
            else:
                return jsonify({"success": "Machine found"}), 200
        except ValueError as e:
            flash(str(e), "error")
            return jsonify({"error": str(e)}), 400
    return redirect('/dashboard')

