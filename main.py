import flet as ft

def main(page: ft.Page):
    page.title = "ATM"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 700

    # --- THE LOGIC DATA (Exactly his) ---
    state = {
        "balance": 10000,
        "pin": 508219,
        "tries": 3,
        "current_action": None
    }

    # --- UI COMPONENTS ---
    display_text = ft.Text("WELCOME", size=24, weight="bold", color="#3b8ed0")
    output_log = ft.ListView(expand=True, spacing=10, padding=20)
    input_field = ft.TextField(label="Enter Details", password=True, can_reveal_password=True, keyboard_type=ft.KeyboardType.NUMBER)
    
    def log(message):
        output_log.controls.append(ft.Text(message, size=16))
        page.update()

    def handle_submit(e):
        val = input_field.value
        input_field.value = ""
        
        # This mirrors his "click 1 for deposit, 2 for withdraw" logic
        if state["current_action"] == None:
            if val == "1":
                state["current_action"] = "deposit_pin"
                log("click 1 for deposit")
                log("eneter your pn")
            elif val == "2":
                state["current_action"] = "withdraw_pin"
                log("click 2 for withdraw")
                log("eneter your pin:")
            elif val == "3":
                state["current_action"] = "balance_pin"
                log("click 3 to check balance")
                log("enter your pin:")
            else:
                log("choose correct one")
        
        # PIN VERIFICATION STAGE
        elif "pin" in state["current_action"]:
            if int(val) == state["pin"]:
                if state["current_action"] == "deposit_pin":
                    state["current_action"] = "deposit_amt"
                    log("eneter the anoumt")
                elif state["current_action"] == "withdraw_pin":
                    state["current_action"] = "withdraw_amt"
                    log("how much money you want to withdraw?")
                elif state["current_action"] == "balance_pin":
                    log(f"your balance is: {state['balance']}")
                    reset_menu()
            else:
                state["tries"] -= 1
                log("INCORRECT PIN")
                log(f"TRIES LEFT: {state['tries']}")
                if state["tries"] <= 0:
                    log("NO MORE TRIES LEFT!")
                    input_field.disabled = True
                    submit_btn.disabled = True
        
        # AMOUNT STAGE
        elif state["current_action"] == "deposit_amt":
            amt = int(val)
            if amt < 0:
                log("cannot deposit negative digits")
            else:
                state["balance"] += amt
                log(f"your balance is: {state['balance']}")
            reset_menu()
            
        elif state["current_action"] == "withdraw_amt":
            amt = int(val)
            if amt < 0:
                log("cannot withdraw negative digits")
            elif amt > state["balance"]:
                log("Insufficient funds!")
            else:
                state["balance"] -= amt
                log(f"Remaining balance: {state['balance']}")
            reset_menu()

        page.update()

    def reset_menu():
        state["current_action"] = None
        log("--- TRANSACTION COMPLETE ---")
        log("1: Deposit | 2: Withdraw | 3: Balance")

    submit_btn = ft.ElevatedButton("Submit", on_click=handle_submit, width=200)

    # Initial Menu Setup
    log("click 1 for deposit")
    log("click 2 for withdraw")
    log("click 3 for check balance")

    # Building the Screen
    page.add(
        ft.Container(
            content=ft.Column([
                display_text,
                ft.Container(output_log, height=300, bgcolor="#1a1a1a", border_radius=10),
                input_field,
                submit_btn
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30
        )
    )

ft.app(target=main)
