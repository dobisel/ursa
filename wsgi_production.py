from ursa import ursa

ursa.configure(files='/etc/ursa.yml')
ursa.initialize_models()
app = ursa
