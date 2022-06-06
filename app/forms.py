from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo


class passwdchangeform(FlaskForm):
    username = StringField('บัญชีผู้ใช้งาน *', validators=[DataRequired()])
    password = PasswordField('รหัสผ่านปัจจุบัน  *',
                             validators=[DataRequired()])
    new_password = PasswordField('รหัสผ่านใหม่', validators=[
                                 DataRequired(), Length(min=8)], render_kw={'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}'})
    confirm_password = PasswordField('ยืนยันรหัสผ่านใหม่', validators=[DataRequired(), Length(min=8),
                                                                       EqualTo('new_password')])
    submit = SubmitField('ส่งข้อมูล')
    recaptcha = RecaptchaField()


class loginform(FlaskForm):
    username = StringField('บัญชีผู้ใช้งาน *', validators=[DataRequired()])
    password = PasswordField('รหัสผ่าน *', validators=[DataRequired()])
    submit = SubmitField('Check')


class registerform(FlaskForm):
    firstname = StringField('Firstname (English)*', validators=[
                            DataRequired(), Length(min=6, max=35)], render_kw={'onchange': 'changeuser()'})
    lastname = StringField('Lastname (English)*', validators=[
                           DataRequired(), Length(min=6, max=35)], render_kw={'onchange': 'changeuser()'})
    idcard = StringField('เลขบัตรประชาชน *', validators=[
                         DataRequired(), Length(min=13, max=13)])
    telephone = StringField('หมายเลขโทรศัพท์ติดต่อภายในกรม *', validators=[
                            DataRequired(), Length(min=4, max=10)])
    mobile = StringField('หมายเลขโทรศัพท์มือถือ *', validators=[
                         DataRequired(), Length(min=9, max=10)])
    email = EmailField('Email *', validators=[
                       DataRequired(),  Length(min=4, max=35)])
    department = StringField('ส่วน/ฝ่าย *', validators=[
        DataRequired(), Length(min=4, max=30)])
    position = StringField('ตำแหน่ง *', validators=[
        DataRequired(), Length(min=4, max=30)])
    office = StringField('สำนัก/กอง *', validators=[
        DataRequired(), Length(min=4, max=30)])
    branch = StringField('สถานที่ปฎิบัติงาน *', validators=[
        DataRequired(), Length(min=4, max=30)])
    level = SelectField('ระดับบุคคลากร *', choices=[(
        'Guest Group', 'นักศึกษาฝึกงาน'), ('TOR', 'TOR'), ('User DNP', 'ข้าราชการ/พนักงานราชการ/ลูกจ้างประจำ'), ('Power User', 'ผู้อำนวยการส่วน'), ('Super User', 'ผู้อำนวยการสำนัก')])

    username = StringField('บัญชีผู้ใช้งาน', validators=[
                           DataRequired()], render_kw={'readonly': True})
    password = PasswordField('รหัสผ่าน *', validators=[DataRequired()], render_kw={
                             'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}'})
    confirm_password = PasswordField('ยืนยันรหัสผ่าน *', validators=[DataRequired(), Length(min=8),
                                                                     EqualTo('password')])
    submit = SubmitField('ส่งข้อมูล')
    recaptcha = RecaptchaField()
