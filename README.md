## Install
    pyvenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate

## Development tasks
    # Run worker
    python manage.py run_huey -w 2

## TODO
- Support dual moccamaster (more thresholds)
- Blink light bulb on finish
- More stats
