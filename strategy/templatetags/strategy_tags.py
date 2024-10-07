from django import template

register = template.Library()

@register.simple_tag
def get_score(scores_dict, pebp_id, criterion_weight_id):
    return scores_dict.get((pebp_id, criterion_weight_id))
