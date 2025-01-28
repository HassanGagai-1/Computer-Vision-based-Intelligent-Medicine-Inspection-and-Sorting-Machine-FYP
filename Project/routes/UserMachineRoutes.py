
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

