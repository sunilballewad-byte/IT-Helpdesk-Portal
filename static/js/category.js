const data = {
    Hardware: {
        Laptop: ["Dell", "HP", "Lenovo", "Surface"],
        Desktop: ["Dell", "HP"],
        Printer: ["HP", "Canon", "Epson"],
        Monitor: ["Dell", "LG"]
    },
    Software: {
        Office: ["Outlook", "Excel", "Word"],
        Windows: ["Windows 11", "Windows 10"],
        ERP: ["NetSuite"]
    },
    Network: {
        WiFi: ["Access Point"],
        Firewall: ["Sophos", "Fortigate"],
        Switch: ["Cisco", "Aruba"]
    }
};

function loadSubCategory() {
    const category = document.getElementById("category").value;
    const subcategory = document.getElementById("subcategory");
    const item = document.getElementById("item");

    // Reset subcategory and item dropdowns
    subcategory.innerHTML = '<option value="">-- Select Sub Category --</option>';
    item.innerHTML = '<option value="">-- Select Item --</option>';

    if (!category || !data[category]) {
        return;
    }

    Object.keys(data[category]).forEach(function (value) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        subcategory.appendChild(option);
    });
}

function loadItems() {
    const category = document.getElementById("category").value;
    const subcategory = document.getElementById("subcategory").value;
    const item = document.getElementById("item");

    // Reset item dropdown
    item.innerHTML = '<option value="">-- Select Item --</option>';

    if (!category || !subcategory || !data[category][subcategory]) {
        return;
    }

    data[category][subcategory].forEach(function (value) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        item.appendChild(option);
    });
}

function loadDescription() {
    const category = document.getElementById("category").value;
    const subcategory = document.getElementById("subcategory").value;
    const item = document.getElementById("item").value;
    const description = document.getElementById("description");

    if (!item) {
        description.value = "";
        return;
    }

    description.value = 
`Category : ${category}
Sub Category : ${subcategory}
Item : ${item}

Issue :

Location :

Error Message :

Impact :

Steps Already Tried :
`;
}

function setPriority() {
    const category = document.getElementById("category").value;
    const priority = document.getElementById("priority");

    switch(category) {
        case "Network":
        case "Access":
            priority.value = "High";
            break;

        case "Hardware":
        case "Software":
        default:
            priority.value = "Medium";
            break;

        case "Email":
            priority.value = "Low";
            break;
    }
}