import click
from Tools import auth
from Tools import patient
from Tools import staff
from Tools import appoint
from Tools import presc
from pyfiglet import Figlet
from time import sleep
import os
@click.command()
def appmgr():
    
    sleep(1)
    click.echo("\n")
    os.system('clear')
    
    
    while(True):
        os.system('clear')
        print (f.renderText('Staff Portal'))
        click.echo("------------------------------")
        click.echo("| Hospital Management System |")
        click.echo("------------------------------")
        click.echo("Please select an option:")
        
        click.echo("1. Patient registration and management")
        click.echo("2. Appointment scheduling")
        click.echo("3. Prescription management")
        click.echo("4. Staff management")
        click.echo("0. Logout and Exit")
        click.echo("\n")
      

        choice = click.prompt("Enter your choice", type=int, default=0, show_choices=True, show_default=False)

        if choice == 1:
            while(True):
                click.echo("\n")
                os.system('clear')
                click.echo("You selected Patient management")
                click.echo("-------------------")
                click.echo("| Patient Manager |")
                click.echo("-------------------")
                click.echo("1. Register a patient")
                click.echo("2. Lookup a patient")
                click.echo("3. All patients")
                click.echo("0. Back to Menu")
                click.echo("\n")
                patientmng_choice = click.prompt("What would you like to do?", type=int, default=0, show_choices=True, show_default=False)
                if patientmng_choice == 1:
                    os.system('clear')
                    click.echo("You selected Register a patient")
                    patient.register_patient()
                    input("press enter to continue..")
                elif patientmng_choice == 2:
                    os.system('clear')
                    click.echo("You selected Lookup a patient")
                    patient.lookup_patient()
                    input("press enter to continue..")
                
                elif patientmng_choice == 3:
                    os.system('clear')
                    click.echo("You selected All patients")
                    patient.get_all_patients()
                    input("press enter to continue..")
                elif patientmng_choice == 0:
                    break

        elif choice == 2:
            click.echo("You selected Appointment scheduling")
            while(True):
                click.echo("\n")
                os.system('clear')
                click.echo("-----------------------")
                click.echo("| Appointment Manager |")
                click.echo("-----------------------")
                click.echo("1. Lookup all appointments")
                click.echo("2. View a patients appointments")
                click.echo("3. View a doctors appointments")
                click.echo("0. Back to Menu")
                click.echo("\n")
                patientmng_choice = click.prompt("What would you like to do?", type=int, default=0, show_choices=True, show_default=False)
                if patientmng_choice == 1:
                    os.system('clear')
                    click.echo("You selected Lookup all appointments")
                    appoint.get_all_appoints()
                    input("press enter to continue..")
                elif patientmng_choice == 2:
                    os.system('clear')
                    click.echo("You selected View a patients appointments")
                    appoint.lookup_patient()
                    input("press enter to continue..")
                elif patientmng_choice == 3:
                    os.system('clear')
                    click.echo("You selected View a doctors appointments")
                    appoint.lookup_doctor()
                    input("press enter to continue..")
                elif patientmng_choice == 0:
                    break

        elif choice == 3:
            while(True):
                click.echo("\n")
                os.system('clear')
                click.echo("You selected Prescription Viewer")
                click.echo("-----------------------")
                click.echo("|    Prescriptions    |")
                click.echo("-----------------------")
                click.echo("1. Lookup a patients Prescriptions")
                click.echo("2. View all Prescriptions")
                click.echo("0. Back to Menu")
                click.echo("\n")
                prescmng_choice = click.prompt("What would you like to do?", type=int, default=0, show_choices=True, show_default=False)
                if prescmng_choice == 1:
                    os.system('clear')
                    click.echo("You selected Lookup a patients Prescriptions")
                    presc.lookup_pres()
                    input("press enter to continue..")
                elif prescmng_choice == 2:
                    os.system('clear')
                    click.echo("You selected View all Prescriptions")
                    presc.get_all_pres()
                    input("press enter to continue..")
                elif prescmng_choice == 0:
                    break
        
        elif choice == 4:
                
            while(True):
                click.echo("\n")
                os.system('clear')
                click.echo("You selected Staff management")
                click.echo("-----------------------")
                click.echo("|     Staff Manager   |")
                click.echo("-----------------------")
                click.echo("1. Lookup a staff member")
                click.echo("2. View all staff")
                click.echo("0. Back to Menu")
                click.echo("\n")
                staffmng_choice = click.prompt("What would you like to do?", type=int, default=0, show_choices=True, show_default=False)
                if staffmng_choice == 1:
                    os.system('clear')
                    click.echo("You selected Lookup a staff member")
                    staff.lookup_staff()
                    input("press enter to continue..")
                elif staffmng_choice == 2:
                    os.system('clear')
                    click.echo("You selected View all staff")
                    staff.get_all_staff()
                    input("press enter to continue..")
                elif staffmng_choice == 0:
                    break
        
        elif choice == 0:
            os.system('clear')
            click.echo("Logging out..")
            sleep(1)
            os.system('clear')
            break
        
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 4.")


def apppatient():
    
    sleep(1)
    click.echo("\n")
    os.system('clear')
    
    
    while(True):
        os.system('clear')
        print (f.renderText('Patient Portal'))
        click.echo("------------------------------")
        click.echo("| Hospital Management System |")
        click.echo("------------------------------")
        click.echo("Please select an option:")

        click.echo("1. Appointment scheduling")
        click.echo("2. Prescription management")
        click.echo("0. Logout and Exit")
        click.echo("\n")
      

        choice = click.prompt("Enter your choice", type=int, default=0, show_choices=True, show_default=False)

        if choice == 1:
            click.echo("You selected Appointment scheduling")
            while(True):
                click.echo("\n")
                os.system('clear')
                click.echo("-----------------------")
                click.echo("| Appointment Manager |")
                click.echo("-----------------------")
                click.echo("1. View appointments")
                click.echo("0. Back to Menu")
                click.echo("\n")
                patientmng_choice = click.prompt("What would you like to do?", type=int, default=0, show_choices=True, show_default=False)
                if patientmng_choice == 1:
                    os.system('clear')
                    click.echo("You selected View appointments")
                    appoint.lookup_my_patient(userID)
                    input("press enter to continue..")
                elif patientmng_choice == 0:
                    break 

        elif choice == 2:
            while(True):
                click.echo("\n")
                os.system('clear')
                click.echo("You selected Prescription Viewer")
                click.echo("-----------------------")
                click.echo("|    Prescriptions    |")
                click.echo("-----------------------")
                click.echo("1. View Prescriptions")
                click.echo("0. Back to Menu")
                click.echo("\n")
                prescmng_choice = click.prompt("What would you like to do?", type=int, default=0, show_choices=True, show_default=False)
                if prescmng_choice == 1:
                    os.system('clear')
                    click.echo("You selected View Prescriptions")
                    presc.lookup_my_patient(userID)
                    input("press enter to continue..")
                elif prescmng_choice == 0:
                    break
        elif choice == 0:
            os.system('clear')
            click.echo("Logging out..")
            sleep(1)
            os.system('clear')
            break
        
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 2.")
if __name__ == "__main__":
    
    f = Figlet(font='slant')
    print (f.renderText('TMU Medical Portal'))
    auth, state, userID = auth.login()
    sleep(1)
    os.system('clear')
    if auth and state == "staff":
        appmgr()
    elif auth and state == "patient":
        apppatient()
        
