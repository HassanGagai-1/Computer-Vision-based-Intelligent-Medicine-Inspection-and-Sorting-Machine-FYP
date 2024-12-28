from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from services.MachineService import MachineService
from flask import render_template
import logging
logger = logging.getLogger(__name__)
machine_bp = Blueprint('machine', __name__)

@machine_bp.route('/addMachine', methods=['GET','POST'])
def addMachine():
    logger.debug("Add machine endpoint called")
    if request.method == 'GET':
        return render_template('dashboard.html')
    try:
        machine_code = request.form.get('machine_code')
        machine_password = request.form.get('machine_password')
        created_by = request.form.get('created_by')
        MachineService.register_machine(machine_code, machine_password,created_by)
        return redirect('/dashboard')
    except ValueError as e:
        return render_template('dashboard.html', error=str(e)), 400
    

@machine_bp.route('/api/getMachines', methods=['GET'])
def getMachines():
    
    logger.debug("Get machines endpoint called")
    machines = MachineService.get_machines()
    
    machine_dicts = [machine.to_dict() for machine in machines]
    
    return jsonify(machine_dicts),200