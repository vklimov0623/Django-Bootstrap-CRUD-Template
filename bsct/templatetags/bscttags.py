from django.core import serializers
from django.template import Library

register = Library()

# -------------------------
# Template Tags
# -------------------------

# CDN Resources
# -------------------------

def netdna_css( path ):
    """
    Returns a link to the named NetDNA-hosted CSS resource.
    """
    return '<link href="//netdna.bootstrapcdn.com/%s" rel="stylesheet">' % path

def netdna_js( path ):
    """
    Returns a script element sourcing the named NetDNA-hosted JavaScript resource.
    """
    return '<script src="//netdna.bootstrapcdn.com/%s"></script>' % path

@register.simple_tag()
def bootstrap_js_cdn(version = '2.3.2'):
    return netdna_js("twitter-bootstrap/%s/js/bootstrap.min.js" % version )

@register.simple_tag()
def bootstrap_cdn( version = '2.3.2'):
    """
    Returns a link to a CDN-hosted Bootstrap minified CSS file.
    """
    return netdna_css('twitter-bootstrap/%s/css/bootstrap-combined.min.css' % version )

@register.simple_tag()
def bootswatch_cdn( theme, version = '2.3.2' ):
    """
    Returns a link to the named CDN-hosted Bootstrap Swatch theme.
    """
    if theme.lower() in [
            "amelia","cerulean","cosmo","cyborg","flatly",
            "journal","readable","simplex","slate","spacelab",
            "spruce","superhero","united"
    ]:
        return netdna_css( "bootswatch/%s/%s/bootstrap.min.css" % (version,theme) )
    raise Exception( "Unrecognized bootswatch theme: '%s'." % theme )


# Meta-data Extractors 
# -------------------------

@register.simple_tag()
def get_verbose_name( object ):
    """
    Returns the verbose name for a model.
    """
    return object._meta.verbose_name

@register.simple_tag()
def get_verbose_name_plural( object ):
    """
    Returns the verbose pluralized name for a model.
    """
    return object._meta.verbose_name_plural


# Pagination Helpers
# -------------------------

@register.simple_tag()
def append_querystring( request, exclude = ['page'] ):
    """
    Returns the query string for the current request.
    """
    ae = '&amp;'
    if request and request.GET:
        return ae + ae.join([ '%s=%s' % (k,v) for k,v in request.GET.iteritems() if k not in exclude ])
    return ''
    


# -------------------------
# Filters
# -------------------------

@register.filter
def model_to_dict( object ):
    """
    Converts a model into a dictionary of its fields and values.
    """
    return serializers.serialize( "python", [object] )[0]['fields']
