from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from services.UserService import UserService
from flask import render_template
from models.users import User
import logging
from extensions import db
import os
from itsdangerous import URLSafeTimedSerializer as Serializer

logger = logging.getLogger(__name__)
user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
	    return render_template('dashboard.html')


@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    print("Current session:", session)
    print("Session get user_ID: ",session.get('user_id'))
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    else:
	    return render_template('dashboard.html')

@user_bp.route('/register', methods=['POST','GET'])
def register():
    logger.debug("UserRoutes.register endpoint called")
    if request.method == 'GET':
        return render_template('signup.html')
    try:
        firstname = request.form.get('firstname')   
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        
        UserService.register_user(firstname, lastname, email, password)
        return redirect(url_for('login'))
    except ValueError as e:
        return render_template('signup.html', error=str(e)), 400

@user_bp.route('/login', methods=['POST','GET'])
def login():
        logger.debug("UserRoutes.login endpoint called")
        if request.method == 'GET':
            return render_template('login.html')
        email = request.form.get('email')
        password = request.form.get('password')
        logger.info('User login attempt')

        if not email or not password:
            flash('Invalid email or password', 'error')
            return render_template('login.html', error='Invalid email or password'), 400

        try:
            user = UserService.login_user(email, password)
            session.permanent = True
            session['user_id'] = user.id
            session.modified = True
            print("Session after login:", dict(session))
            return redirect(url_for('user.dashboard'))

        except ValueError:
            flash('Invalid credentials', 'error')
            return render_template('login.html', error='Invalid email or password'), 400

@user_bp.route('/logout', methods=['GET'])
def logout():
        session.clear()
        flash("You have been successfully logged out!", "Info")
        return redirect(url_for('user.login'))
    
    
@user_bp.route('/forgetPassword', methods=['GET', 'POST'])
def forgetPass():
    if request.method == 'POST':
      
        Uemail = request.form.get("username", False)
        print("User mail is", Uemail)
        userData = UserService.get_user_email_profile(Uemail)
        
        print("JABBA: ",userData)
        if userData:
            if userData.email == Uemail:
                user_data = {
                    'user_id': Uemail,
                }

                token   = UserService.get_secret_token(user_data)
                # print("HTML Content:", HTML_CONTENT)
                reset_url = url_for('user.resetPass', token=token, _external=True, _scheme='http')
                # send_email(Uemail, 'Password Reset', HTML_CONTENT)
                HTML_CONTENT = f'''
                    <html>
                    <head>
                        <title></title>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                        <style type="text/css">
                            /* FONTS */
                            @media screen {{
                                @font-face {{
                                    font-family: 'Lato';
                                    font-style: normal;
                                    font-weight: 400;
                                    src: local('Lato Regular'), local('Lato-Regular'),
                                    url(https://fonts.gstatic.com/s/lato/v11/qIIYRU-oROkIk8vfvxw6QvesZW2xOQ-xsNqO47m55DA.woff) format('woff');
                                }}
                                @font-face {{
                                    font-family: 'Lato';
                                    font-style: normal;
                                    font-weight: 700;
                                    src: local('Lato Bold'), local('Lato-Bold'),
                                    url(https://fonts.gstatic.com/s/lato/v11/qdgUG4U09HnJwhYI-uK18wLUuEpTyoUstqEm5AMlJo4.woff) format('woff');
                                }}
                                @font-face {{
                                    font-family: 'Lato';
                                    font-style: italic;
                                    font-weight: 400;
                                    src: local('Lato Italic'), local('Lato-Italic'),
                                    url(https://fonts.gstatic.com/s/lato/v11/RYyZNoeFgb0l7W3Vu1aSWOvvDin1pK8aKteLpeZ5c0A.woff) format('woff');
                                }}
                                @font-face {{
                                    font-family: 'Lato';
                                    font-style: italic;
                                    font-weight: 700;
                                    src: local('Lato Bold Italic'), local('Lato-BoldItalic'),
                                    url(https://fonts.gstatic.com/s/lato/v11/HkF_qI1x_noxlxhrhMQYELO3LdcAZYWl9Si6vvxL-qU.woff) format('woff');
                                }}
                            }}
                            /* CLIENT-SPECIFIC STYLES */
                            body, table, td, a {{
                                -webkit-text-size-adjust: 100%;
                                -ms-text-size-adjust: 100%;
                            }}
                            table, td {{
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                            }}
                            img {{
                                -ms-interpolation-mode: bicubic;
                            }}
                            /* RESET STYLES */
                            img {{
                                border: 0;
                                height: auto;
                                line-height: 100%;
                                outline: none;
                                text-decoration: none;
                            }}
                            table {{
                                border-collapse: collapse !important;
                            }}
                            body {{
                                height: 100% !important;
                                margin: 0 !important;
                                padding: 0 !important;
                                width: 100% !important;
                            }}
                            /* iOS BLUE LINKS */
                            a[x-apple-data-detectors] {{
                                color: inherit !important;
                                text-decoration: none !important;
                                font-size: inherit !important;
                                font-family: inherit !important;
                                font-weight: inherit !important;
                                line-height: inherit !important;
                            }}
                            /* ANDROID CENTER FIX */
                            div[style*="margin: 16px 0;"] {{
                                margin: 0 !important;
                            }}
                        </style>
                    </head>
                    <body style="background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;">
                        <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">Hi!</div>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tbody>
                                <tr>
                                    <td bgcolor="#C62B5B" align="center">
                                        <table border="0" cellpadding="0" cellspacing="0" width="480">
                                            <tbody>
                                                <tr>
                                                    <td align="center" valign="top" style="padding: 40px 10px 40px 10px;">
                                                        <a href="https://pifs.lts.com.fj" target="_blank"></a>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#C62B5B" align="center" style="padding: 0px 10px 0px 10px;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="480">
                                            <tbody>
                                                <tr>
                                                    <td bgcolor="#ffffff" align="center" valign="top" style="padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;">
                                                        <h1 style="font-size: 32px; font-weight: 400; margin: 0;">Forgot Your Password?</h1>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="480">
                                            <tbody>
                                                <tr>
                                                    <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 40px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                                        <p style="margin: 0;">Hey {Uemail},<br><br>Please tap the button below or click here to change your password.<br><br>If you didn't request to reset the password, don't worry. Just ignore this email and the link will expire on its own.<br><br>Have a nice day.<br>Stay Safe!<br></p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td bgcolor="#ffffff" align="left">
                                                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td bgcolor="#ffffff" align="center" style="padding: 20px 30px 60px 30px;">
                                                                        <table border="0" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" style="border-radius: 3px;" bgcolor="#C62B5B">
                                                                                    <a href="{reset_url}" target="_blank" style="font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #C62B5B; display: inline-block;">
                                                                                    Reset Password</a>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#f4f4f4" align="center" style="padding: 16px 10px 0px 10px;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="480">
                                            <tbody>
                                                <tr>
                                                    <td bgcolor="#f4f4f4" align="left" style="padding: 0px 30px 16px 30px;color: #666666;font-family: 'Lato', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;line-height: 18px;">
                                                        <p style="margin: 0;">You received this email because your account password is being resetted</p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td bgcolor="#f4f4f4" align="left" style="padding: 0px 30px 30px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 18px;">
                                                        <p style="margin: 0;">Suite # 6B-3/4, 6th Floor, Fakhri Trade Center, Shahra-e-Liaquat, KHI</p>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </body>
                    </html>
                '''
               
                UserService.send_email(Uemail, 'Password Reset', HTML_CONTENT)
                print(token)
                flash('Reset email sent Successfully!', 'success')
                return redirect(url_for('user.forgetPass'))
            else:
                flash('Email Does not exist !', 'danger')
                return redirect(url_for('user.forgetPass'))

        else:
            flash('Email Does not exist !', 'danger')
            return redirect(url_for('user.forgetPass'))

    return render_template('forgetpass.html')


@user_bp.route('/updateUser', methods=['POST','GET'])
def updateUser():
    logger.debug("UserRoutes.updateUser endpoint called")
    if request.method == 'GET':
        return render_template('dashboard.html')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    current_user_id = session.get('user_id')

    if not current_user_id:
        flash("Please log in first.", "error")
        return redirect('/login')
    try:
        logger.debug("Update user")
        UserService.update_user(current_user_id, firstname, lastname, email )
        flash("User updated successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect('/dashboard')

@user_bp.route('/resetpass/<token>',methods=['GET','POST'])
def resetPass(token):
    user_data_json=verify_secret_token(token)
    print(user_data_json) 
    user_id = user_data_json.get('user_id')
    session['userID']=user_id
    return render_template('changepass.html',form=True)

@user_bp.route('/changepass', methods=['GET','POST'])
def changepass():
    if request.method == 'POST':
       
        new_password = request.form.get('password')
    
        re_new_password = request.form.get('repassword')

        user_mail = session.get('userID')
    
        if not user_mail:        
            return redirect('/login')  

        
        if new_password == re_new_password:
            UserService.changepassword(user_mail, new_password)
            return render_template('changepass.html', changed=True)
        else:
            return render_template('changepass.html', unchanged=True)

    return render_template('changepass.html', form=True)


    
    
    



def verify_secret_token(token):
    serial = Serializer(os.getenv('FLASK_SECRET_KEY', 'fallbacksecret'))
    
    try:
        data = serial.loads(token, max_age=100000)
        print("Data:",data)
        return data
    except Exception as e:
        print("Token is invalid or expired:", str(e))
        return None
    



@user_bp.route('/api/getUserProfile', methods=['GET']) 
def getUserProfile():
    
    current_user_id = session.get('user_id')
    
    logger.debug(f"Current user id: {current_user_id}")
    if not current_user_id:
        return jsonify({"error": "Unauthorized access"}), 401

    user = UserService.get_user_profile(current_user_id)
    
    logger.debug(f"User Founded email is : {user.email} + {user.firstname}")
    
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404


@user_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    User.query.get(user_id)
    return render_template('profile.html')

