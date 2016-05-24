## Install
    pyvenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate

## Development tasks
    # Run worker
    python manage.py run_huey -w 2

## TODO
- Fix threshold numbers
- Fix translations, change to first person ("I finished n minutes ago, sorry i took so long")
- Support dual moccamaster (more thresholds)
- Blink light bulb on finish
- More stats
