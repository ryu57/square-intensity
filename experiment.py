import expyriment
import os
import pandas as pd
import time
import random



directory_path = "data/"
os.makedirs(directory_path, exist_ok=True)

# Start Expyriment
exp = expyriment.design.Experiment(name="High Intensity Task")

# expyriment.control.set_develop_mode(True)
expyriment.control.initialize(exp)


exp.mouse.show_cursor()
clock = expyriment.misc.Clock()
kb = expyriment.io.Keyboard()

# DataFrame
df_pdata = pd.DataFrame(columns=["Participant Code", "Elapsed Time (Seconds)", "Number of Squares", "Number of Switches","Display Time", "Correct"])

# Button Canvas
canvas = expyriment.stimuli.Canvas((700, 700))

# Button Data

intensity_dict = {1: 2.4, 2: 2.2, 3: 1.8, 4: 1.5, 5: 1.3}

def generate_array(length, intensity):
    switches = int(length // intensity)
    # print("switches: ", switches)
    if switches >= length:
        raise ValueError("Number of switches must be less than the length of the array")

    # Initialize the array with random starting value (0 or 1)
    array = [random.choice([0, 1])]
    
    # Generate the rest of the array
    current_value = array[0]
    for _ in range(1, length):
        if switches > 0 and random.random() < (switches / (length - len(array))):
            current_value = 1 - current_value  # Switch between 0 and 1
            switches -= 1
        array.append(current_value)
    
    return array


def plot_buttons(text, canvas):
    instruction_text = expyriment.stimuli.TextLine(f"How many {text} squares?", text_size=30, position=(0,150))
    buttons_top = [expyriment.stimuli.Rectangle(size=(50, 50), position=(x * 60 - 310, 0), colour=(255,255,255)) for x in range(11)]
    buttons_bottom = [expyriment.stimuli.Rectangle(size=(50, 50), position=(x * 60 - 280, -80), colour=(255,255,255)) for x in range(10)]
    buttons = buttons_top + buttons_bottom
    for i, button in enumerate(buttons_top):
        button.plot(canvas)
        text = expyriment.stimuli.TextLine(text=str(i), position=(i * 60 - 310, 0), text_colour=(0,0,0))
        text.plot(canvas)
    for i, button in enumerate(buttons_bottom):
        button.plot(canvas)
        text = expyriment.stimuli.TextLine(text=str(i + 11), position=(i * 60 - 280, -80), text_colour=(0,0,0))
        text.plot(canvas)

    instruction_text.plot(canvas)
    canvas.present()

    answer = None
    while answer is None:
        button_pressed, pos, rt = exp.mouse.wait_press()
        for i, button in enumerate(buttons):
            if button.overlapping_with_position(pos):
                answer = i
                break
    canvas.unload()
    return answer
    


def run_experiment():
    # Non Trial Canvas for displaying instructions
    instruction_canvas = expyriment.stimuli.Canvas((700, 700))
    # Instruction 1
    instruction_header = expyriment.stimuli.TextLine("Press ESC to Quit Early",
                                                     text_size=60,
                                                     position=(0, 00))

    instruction_prompt = expyriment.stimuli.TextLine(
        "Press Spacebar to Continue...", text_size=30, position=(0, -200))

    instruction_header.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    kb.wait_char(' ')
    instruction_canvas.unload()


    # Ask for participant code
    name = ""
    while name == "":
        name = expyriment.io.TextInput("Participant code, to be filled by the RA:", message_text_size=30, user_text_size=30).get()


    # Instruction 1
    instruction_header = expyriment.stimuli.TextLine("Instructions", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine("You will be shown squares", text_size=30, position=(0,150))
    instruction_text1 = expyriment.stimuli.TextLine("at the centre of your screen:", text_size=30, position=(0,100))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))
    shape = expyriment.stimuli.Rectangle((70,70), position=(0,0), colour=(255,255,255))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_text1.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    shape.plot(instruction_canvas)
    instruction_canvas.present()
    kb.wait_char(' ')
    instruction_canvas.unload()

    # Instruction 2
    instruction_header = expyriment.stimuli.TextLine("Instructions", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine("The squares can either be large or small", text_size=30, position=(0,130))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))
    shape = expyriment.stimuli.Rectangle((70,70), position=(-70,0), colour=(255,255,255))
    shape_extra = expyriment.stimuli.Rectangle((110,110), position=(70, 0), colour=(255,255,255))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    shape.plot(instruction_canvas)
    shape_extra.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    kb.wait_char(' ')
    instruction_canvas.unload()

    
    
    # Instruction 3
    instruction_header = expyriment.stimuli.TextLine("Instructions", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine("Count the number of", text_size=40, position=(0,100))
    instruction_text1 = expyriment.stimuli.TextLine("small and large squares.", text_size=40, position=(0,30))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_text1.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    fs = expyriment.stimuli.FixCross(size=(25, 25), line_width=3, colour=(127, 127, 127))
    blank = expyriment.stimuli.BlankScreen()
    button_delay = 300

    repeat = True
    while repeat:
        # Instruction 4
        instruction_header = expyriment.stimuli.TextLine("Practice Round", text_size=60, position=(0,240))
        instruction_text1 = expyriment.stimuli.TextLine("When you are ready", text_size=30, position=(0,-150))
        instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Start...", text_size=30, position=(0,-200))

        instruction_header.plot(instruction_canvas)
        instruction_text1.plot(instruction_canvas)
        instruction_prompt.plot(instruction_canvas)
        instruction_canvas.present()
        instruction_canvas.unload()
        kb.wait_char(' ')

        

        # Practice Trial
        practice_trial = [0,1,1,0,0,0,1,0,0,1]
        for i in practice_trial:
            fs.present()
            clock.wait(250)
            canvas.unload()

            if i == 0:
                shape = expyriment.stimuli.Rectangle((70, 70), position=(0, 0), colour=(255, 255, 255))
            else:
                shape = expyriment.stimuli.Rectangle((110, 110), position=(0, 0), colour=(255, 255, 255))

            shape.plot(canvas)
            canvas.present()
            clock.wait(800)
            canvas.unload()

        small_answer = plot_buttons("SMALL", canvas)
        blank.present(canvas)
        clock.wait(button_delay)
        canvas.unload()

        big_answer = plot_buttons("BIG", canvas)
        blank.present(canvas)
        clock.wait(button_delay)
        canvas.unload()

        small_correct = len(practice_trial) - sum(practice_trial)
        big_correct = sum(practice_trial)

        # Instruction 5
        instruction_header = expyriment.stimuli.TextLine("Practice Results", text_size=60, position=(0,240))
        
        if small_correct == int(small_answer) and big_correct == int(big_answer):
            instruction_text = expyriment.stimuli.TextLine("Your answer was:", text_size=40, position=(0,150))
            instruction_text1 = expyriment.stimuli.TextLine("Correct!", text_size=40, position=(0,100), text_colour=(0,255,0))
        else:
            instruction_text = expyriment.stimuli.TextLine("Your answer was:", text_size=40, position=(0,150))
            instruction_text1 = expyriment.stimuli.TextLine("Incorrect!", text_size=40, position=(0,100), text_colour=(255,0,0))


        instruction_prompt2 = expyriment.stimuli.TextLine(
            "Press R to Try Again", text_size=30, position=(0, -150))
        instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Proceed...", text_size=30, position=(0,-200))

        instruction_header.plot(instruction_canvas)
        instruction_text.plot(instruction_canvas)
        instruction_text1.plot(instruction_canvas)
        instruction_prompt.plot(instruction_canvas)
        instruction_prompt2.plot(instruction_canvas)
        instruction_canvas.present()
        instruction_canvas.unload()
        key, rt = kb.wait_char(["r", " "])
        if key == " ":
            repeat = False

    # Instruction 6
    instruction_text1 = expyriment.stimuli.TextLine("The Actual Task is Next", text_size=40, position=(0,80))
    instruction_text2 = expyriment.stimuli.TextLine("If you have any questions for the RA",
                                                    text_size=30,
                                                    position=(0, 20))
    instruction_text3 = expyriment.stimuli.TextLine(
        "Now is the time",
        text_size=30,
        position=(0, -20))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))

    instruction_text3.plot(instruction_canvas)
    instruction_text2.plot(instruction_canvas)
    instruction_text1.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    # Instruction 7
    instruction_text1 = expyriment.stimuli.TextLine("When you are ready", text_size=30, position=(0,0))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Start...", text_size=30, position=(0,-50))

    instruction_text1.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    # Trial
    participant_code_data = []
    num_squares_data = []
    num_switches_data = []
    display_time_data = []
    elapsed_time_data = []
    correct_data = []

    number_of_trials = 60 #number of trials = 60
    num_correct_end_early = 35
    number_of_squares = 12
    switchintensity = 1
    display_time = 800
    trial_start_time = time.time()
    num_correct = 0
    trial_complete = False

    shape_small = expyriment.stimuli.Rectangle((70, 70), position=(0, 0), colour=(220, 220, 220))
    shape_large = expyriment.stimuli.Rectangle((110, 110), position=(0, 0), colour=(220, 220, 220))
    

    for j in range(number_of_trials):
        # print("trial: ", j)
        trial_format = generate_array(number_of_squares,intensity_dict[switchintensity])
        for i in trial_format:
            fs.present()
            clock.wait(250)
            canvas.unload()

            if i == 0:
                shape_small.plot(canvas)
            else:
                shape_large.plot(canvas)

            canvas.present()
            clock.wait(display_time)
            canvas.unload()

        small_correct = len(trial_format) - sum(trial_format)
        big_correct = sum(trial_format)

        # print("small_correct: ", small_correct)
        # print("big_correct: ", big_correct)
        

        small_answer = plot_buttons("SMALL", canvas)
        blank.present(canvas)
        clock.wait(button_delay)
        canvas.unload()

        big_answer = plot_buttons("BIG", canvas)
        blank.present(canvas)
        clock.wait(button_delay)
        canvas.unload()

        # print("small_answer: ", small_answer)
        # print("big_answer: ", big_answer)
        small_correct = len(trial_format) - sum(trial_format)
        big_correct = sum(trial_format)

        # Instruction 5
        instruction_header = expyriment.stimuli.TextLine("Results", text_size=60, position=(0,240))

        correct_previous_trial = small_correct == int(small_answer) and big_correct == int(big_answer)
        if correct_previous_trial:
            num_correct += 1
        

        
        current_time = time.time() - trial_start_time
        elapsed_time_data.append(round(current_time,3))
        display_time_data.append(display_time)
        participant_code_data.append(name)
        num_squares_data.append(number_of_squares)
        num_switches_data.append(int(number_of_squares // intensity_dict[switchintensity]))

        if current_time > 900 or num_correct == num_correct_end_early:
            trial_complete = True


        # Adjust difficulty based on correctness
        if correct_previous_trial:
            if number_of_squares < 17 and switchintensity <= 5:
                number_of_squares += 1
            elif number_of_squares == 17 and switchintensity < 5:
                number_of_squares -= 6
                switchintensity += 1
            elif number_of_squares == 17 and switchintensity == 5:
                number_of_squares = 17
                switchintensity = 5
            display_time -= 20  # Decrease duration if correct

            instruction_text = expyriment.stimuli.TextLine("Your answer was:", text_size=40, position=(0,150))
            instruction_text1 = expyriment.stimuli.TextLine("Correct!", text_size=40, position=(0,100), text_colour=(0,255,0))
            if j == number_of_trials - 1 or trial_complete:
                instruction_prompt2 = expyriment.stimuli.TextLine("The task is complete", text_size=30, position=(0, -150))
            else:
                instruction_prompt2 = expyriment.stimuli.TextLine("The next trial will be harder", text_size=30, position=(0, -150), text_colour=(255,0,0))
            correct_data.append(1)
        else:
            if number_of_squares == 11 and switchintensity == 1:
                number_of_squares = 11
                switchintensity = 1
            elif number_of_squares == 11 and switchintensity > 1:
                number_of_squares += 6
                switchintensity -= 1
            elif number_of_squares > 11 and switchintensity >= 1:
                number_of_squares -= 1
            display_time += 20 # Increase duration if incorrect

            instruction_text = expyriment.stimuli.TextLine("Your answer was:", text_size=40, position=(0,150))
            instruction_text1 = expyriment.stimuli.TextLine("Incorrect!", text_size=40, position=(0,100), text_colour=(255,0,0))
            if j == number_of_trials - 1 or trial_complete:
                instruction_prompt2 = expyriment.stimuli.TextLine("The task is complete", text_size=30, position=(0, -150))
            else:
                instruction_prompt2 = expyriment.stimuli.TextLine("The next trial will be easier", text_size=30, position=(0, -150), text_colour=(0,255,0))
            correct_data.append(0)

        # print("=====================================")

        instruction_header.plot(instruction_canvas)
        instruction_text.plot(instruction_canvas)
        instruction_text1.plot(instruction_canvas)
        instruction_prompt2.plot(instruction_canvas)
        instruction_canvas.present()

        instruction_header.unload()
        instruction_text.unload()
        instruction_text1.unload()
        instruction_prompt2.unload()
        instruction_canvas.unload()
        clock.wait(2000)

        if trial_complete:
            break

    df_pdata["Participant Code"] = participant_code_data
    df_pdata["Elapsed Time (Seconds)"] = elapsed_time_data
    df_pdata["Number of Squares"] = num_squares_data
    df_pdata["Number of Switches"] = num_switches_data
    df_pdata["Display Time"] = display_time_data
    df_pdata["Correct"] = correct_data

    # Save data
    final_file_directory = "data/"
    final_file_name = f"HiInten_data_{name}.csv"
    df_pdata.to_csv(final_file_directory + final_file_name, index=False)



    # Instruction 10
    instruction_header = expyriment.stimuli.TextLine("Please raise your hand",
                                                     text_size=55,
                                                     position=(0, 240))
    instruction_text = expyriment.stimuli.TextLine(
        f"The RA will prepare the next task", text_size=40, position=(0, 150))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char('\r\n')

    expyriment.control.end()

if __name__ == "__main__":
    run_experiment()
