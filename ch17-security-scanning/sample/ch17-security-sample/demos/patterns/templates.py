"""Jinja2 without autoescape, and templates built from user input."""

from jinja2 import Environment, select_autoescape

comment = "<script>steal(document.cookie)</script>"
raw = Environment().from_string("<p>{{ comment }}</p>")
print("Environment():                 ", raw.render(comment=comment))
safe = Environment(autoescape=select_autoescape(default_for_string=True))
print("select_autoescape():           ", safe.from_string("<p>{{ c }}</p>").render(c=comment))

user_template = "Hello {{ 7 * 7 }}"
print("Template from user input:      ", Environment().from_string(user_template).render())
print("User input as data:            ",
      safe.from_string("Hello {{ name }}").render(name=user_template))
