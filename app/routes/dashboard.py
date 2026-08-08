from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html', user=current_user)