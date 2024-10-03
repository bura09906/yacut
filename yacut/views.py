from flask import abort, flash, redirect, render_template

from . import app
from .error_handlers import ErrorCreatingShortLink, InvalidShortError
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    context = {'form': form}
    if form.validate_on_submit():
        try:
            urlmap = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data or URLMap.get_unique_short_id(),
            )
            created_urlmap = urlmap.save()
            context['short_link'] = created_urlmap.short
            return render_template('yacut.html', **context)
        except InvalidShortError as error:
            flash(error.message)
        except ErrorCreatingShortLink as error:
            flash(error.message)

    return render_template('yacut.html', **context)


@app.route('/<string:short_link>')
def redirect_original_link(short_link):
    original_link = URLMap.get_by_field_short(short_link)
    if original_link is None:
        abort(404)
    return redirect(original_link.original)