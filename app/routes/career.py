import json
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask import send_file
from app.services.pdf_service import generate_report_pdf

from app.extensions import db
from app.models.career_report import CareerReport
from app.utils.forms import CareerAdvisorForm
from app.services.gemini_service import generate_career_advice, GeminiServiceError

career_bp = Blueprint('career', __name__, url_prefix='/career')


@career_bp.route('/advisor', methods=['GET', 'POST'])
@login_required
def advisor():
    form = CareerAdvisorForm()

    if form.validate_on_submit():
        profile_data = {
            'education_level': form.education_level.data,
            'marks_cgpa': form.marks_cgpa.data,
            'interests': form.interests.data,
            'skills': form.skills.data,
            'career_goal': form.career_goal.data,
            'budget': form.budget.data,
            'country': form.country.data,
            'preferred_industry': form.preferred_industry.data,
        }

        try:
            result = generate_career_advice(profile_data)
        except GeminiServiceError as e:
            flash(f'AI service error: {e}', 'danger')
            return render_template('career/advisor.html', form=form)

        report = CareerReport(
            user_id=current_user.id,
            education_level=profile_data['education_level'],
            marks_cgpa=profile_data['marks_cgpa'],
            interests=profile_data['interests'],
            skills=profile_data['skills'],
            career_goal=profile_data['career_goal'],
            budget=profile_data['budget'],
            country=profile_data['country'],
            preferred_industry=profile_data['preferred_industry'],
            result_json=json.dumps(result)
        )
        db.session.add(report)
        db.session.commit()

        return redirect(url_for('career.report_detail', report_id=report.id))

    return render_template('career/advisor.html', form=form)


@career_bp.route('/report/<int:report_id>')
@login_required
def report_detail(report_id):
    report = CareerReport.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    result = json.loads(report.result_json)
    return render_template('career/report.html', report=report, result=result)


@career_bp.route('/history')
@login_required
def history():
    reports = CareerReport.query.filter_by(user_id=current_user.id) \
        .order_by(CareerReport.created_at.desc()).all()
    return render_template('career/history.html', reports=reports)

@career_bp.route('/report/<int:report_id>/download')
@login_required
def download_report(report_id):
    report = CareerReport.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    result = json.loads(report.result_json)
    pdf_buffer = generate_report_pdf(report, result)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f'CareerCompass_Report_{report_id}.pdf',
        mimetype='application/pdf'
    )