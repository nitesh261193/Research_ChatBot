import yaml

import train

FEEDBACK_DATA_SEP = "|"


def improve_using_feedback():
    retrain_needed = False

    with open('domain.yml', 'r') as domain:
        domain_data = yaml.load(domain)

    with open('feedback.dat', 'r+') as feedback:
        for line in feedback.readlines():
            intent, prev_opt, new_opt = line.strip().split(FEEDBACK_DATA_SEP)
            intent = intent.strip()
            prev_opt = prev_opt.strip()
            new_opt = new_opt.strip()

            action = f'utter_{intent}'
            if action not in domain_data['actions']:
                print(f'WARN: intent: [{intent}] is not mapped to a corresponding action in domain.yml')
                continue
            if action not in domain_data['templates']:
                print(f"WARN: action: [{action}] for intent: [{intent}] don't have any templates configured")
                continue

            action_templates = domain_data['templates'][action]
            prev_opt_found = False
            for action_template in action_templates:
                if action_template['text'] == prev_opt:
                    retrain_needed = True  # Even if we updated one option we need retraining
                    prev_opt_found = True
                    action_template['text'] = new_opt
                    break
            if prev_opt_found:
                print(f'[{prev_opt}] is replaced to [{new_opt}] in action:[{action}]')
            else:
                print(f"WARN: [{prev_opt}] is not found in the templates of action:[{action}]")

    print('Rewriting domain.yaml...')
    with open('domain.yml', 'w+') as domain:
        yaml.dump(domain_data, domain)

    with open('feedback.dat', 'w+') as feedback:
        feedback.write('')

    if retrain_needed:
        print('Retraining model after updating domain.yml with feedback')
        train.train()


def update_feed_back(intent, prev_opt, new_opt):
    with open('feedback.dat', 'a+') as feedback:
        feedback.write(f'{intent}{FEEDBACK_DATA_SEP}{prev_opt}{FEEDBACK_DATA_SEP}{new_opt}\n')
