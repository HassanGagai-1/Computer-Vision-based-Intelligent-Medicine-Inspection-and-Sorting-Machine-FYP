from flask import Blueprint, render_template, request, redirect, flash, session
from services.MachineService import MachineService
from flask import render_template
import logging
from decorators.totp import totp_required

logger = logging.getLogger(__name__)
machine_bp = Blueprint('machine', __name__)

@machine_bp.route('/addMachine', methods=['GET','POST'])
@totp_required
def addMachine():
    logger.debug("Add machine endpoint called")
    if request.method == 'GET':
        return render_template('dashboard.html')
    machine_code = request.form.get('machine_code')
    created_by = request.form.get('created_by')
    current_user_id = session.get('user_id')

    if not current_user_id:
        flash("Please log in first.", "error")
        return redirect('/login')
    try:
        logger.debug("Register machine")

        MachineService.register_machine(machine_code,created_by,current_user_id)
        flash("Machine added successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect('/dashboard')