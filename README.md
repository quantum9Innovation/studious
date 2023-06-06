# studious

A time manager for people without time

---

Install it with:

```sh
git clone https://github.com/quantum9Innovation/studious
cd studious
pip install -r requirements.txt
pip install -e .
```

Then, try

```sh
studious --help
```

to get available options.

## Commands

Available commands are:

```txt
schedule
pick
add
delete
modify
log
logs
list
view
about
```

Studious works by storing activities (created by the `add` command) and then receiving logs (created by the `log` command).
It then works out which activity you should work on (with `pick`) to keep all activities balanced according to the percentages specified.
This is the basis for its recommendation algorithm.

**This project is still in beta**  
Parts of this project may change without warning or proper documentation.
