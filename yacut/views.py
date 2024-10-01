from flask import abort, flash, redirect, render_template

from . import app, db
from .core import check_exist_urlmap, check_short_link, get_unique_short_id
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    context = {'form': form}
    if form.validate_on_submit():
        original_link = form.original_link.data
        short_link = form.custom_id.data
        urlmap = check_exist_urlmap(original_link)

        if not short_link and not urlmap:
            short_link = get_unique_short_id()
        elif not short_link and urlmap:
            context['short_link'] = urlmap.short
            return render_template('yacut.html', **context)
        elif check_short_link(short_link):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', **context)

        urlmap = URLMap(
            original=original_link,
            short=short_link,
        )
        db.session.add(urlmap)
        db.session.commit()
        context['short_link'] = short_link
        return render_template('yacut.html', **context)

    return render_template('yacut.html', **context)


@app.route('/<string:short_link>')
def redirect_original_link(short_link):
    original_link = URLMap.query.filter_by(short=short_link).first()
    if original_link is None:
        abort(404)
    return redirect(original_link.original)