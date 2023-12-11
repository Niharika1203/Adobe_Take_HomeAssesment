import json
from datetime import datetime

def deduplicate_leads(leads):
    unique_leads = {}
    log_changes = []

    for lead in reversed(leads):
        lead_id = lead["_id"]
        if lead_id not in unique_leads or lead["entryDate"] > unique_leads[lead_id]["entryDate"]:
            unique_leads[lead_id] = lead

    for original_lead, new_lead in zip(leads, unique_leads.values()):
        log_changes.append(generate_change_log(original_lead, new_lead))

    return list(unique_leads.values()), log_changes

def generate_change_log(original_lead, new_lead):
    log_entry = {
        "source_record": original_lead,
        "output_record": new_lead,
        "field_changes": []
    }

    for key, value in original_lead.items():
        if new_lead[key] != value:
            log_entry["field_changes"].append({
                "field": key,
                "value_from": value,
                "value_to": new_lead[key]
            })

    return log_entry

if __name__ == "__main__":
    input_file = "leads.json"
    output_file = "deduplicated_leads.json"
    log_file = "log_changes.json"

    # load leads.json from file
    with open(input_file, 'r') as file:
        leads_data = json.load(file)
    leads = leads_data['leads']

    deduplicated_leads, log_changes = deduplicate_leads(leads)

    # save output to file
    data = {"leads": deduplicated_leads}
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=2)

    print(f"\nDeduplicated leads saved to {output_file}.")

    # Save the log of changes
    logs = {"logs": log_changes}
    with open(log_file, 'w') as file:
        json.dump(logs, file, indent=2)

    print(f"\nLogs of the changes saved to {log_file}.")

    # Uncomment to print the log of changes:
    # print("Log of Changes:")
    # for log_entry in log_changes:
    #     print(json.dumps(log_entry, indent=2))
