import pandas as pd
import numpy as np

#
start_date=int(2008)
end_date=int(2025)
#Static Infos

np.random.seed(42) # Set random seed for reproducibility

# Define the number of samples
n_samples = 100000

intervall_etudiant_Amount=[500,10000]
intervall_salaire_Amount=[3000,30000]
intervall_professionnel_Amount=[15000,150000]
intervall_joint_Amount=[5000,100000]
intervall_epargne_Amount=[5000,50000]

Villes = [
    "Agadir", "Ahfir", "Ain Harrouda", "Ait Melloul", "Ajdir", "Al Hoceïma", "Assilah", "Azemmour", "Azilal",
    "Beni Mellal", "Ben Guerir", "Berkane", "Berrechid", "Boujdour", "Bouznika",
    "Casablanca", "Chefchaouen", "Chichaoua", "Dakhla",
    "El Hajeb", "El Jadida", "Errachidia", "Essaouira", "Fès",
    "Fquih Ben Salah", "Guelmim", "Guercif",
    "Ifrane", "Imzouren", "Inezgane", "Jerada", "Kénitra", "Ksar El Kebir", "Khémisset", "Khénifra", "Khouribga",
    "Laâyoune", "Larache",
    "Marrakech", "Martil", "Meknès", "Midar", "Midelt", "Mohammédia",
    "Nador",
    "Ouarzazate", "Ouezzane", "Oujda",
    "Rabat", "Rehamna",
    "Safi", "Salé", "Sefrou", "Settat", "Sidi Bennour", "Sidi Ifni", "Sidi Kacem", "Sidi Slimane", "Skhirat", "Souk El Arbaa",
    "Tamesna", "Tan-Tan", "Tanger", "Taounate", "Taourirt", "Tarfaya", "Taroudant", "Tata", "Taza", "Témara", "Tétouan", "Tiflet", "Tinghir", "Tiznit",
    "Youssoufia", "Zagora"
]
comptes_bancaires = [
    "d’épargne",
    "professionnel",
    "joint",
    "salaire",
    "étudiant"
]

transfer_type=['TPE', 'Desktop', 'Phone', 'DAB'] #DAB is ATM ( mean transation from GAP-Bank Agent) 

merchant_category_codes = {
    # Alimentation & Restaurants 🍔
    "5411": "Épiceries et supermarchés",
    "5812": "Restaurants",
    "5813": "Bars et discothèques",
    "5814": "Fast-food",

    # Transport & Voyages ✈️
    "4111": "Services de transport en commun",
    "4511": "Compagnies aériennes",
    "4722": "Agences de voyage",
    "5541": "Stations-service",

    # Santé & Médical 🏥
    "8011": "Médecins",
    "8021": "Dentistes",
    "8062": "Hôpitaux",
    "8099": "Services médicaux divers",

    # Achats & E-commerce 🛒
    "5311": "Grands magasins",
    "5691": "Magasins de vêtements",
    "5732": "Magasins d'électronique",
    "5942": "Librairies",

    # Services financiers 💰
    "6011": "Distributeurs automatiques de billets (ATM)",
    "6051": "Cryptomonnaies",
    "6211": "Courtiers en bourse",
    "6300": "Assurances"
}

job_statuses_list = [
    "Salarié",
    "Stagiaire",
    "Intérimaire",
    "Fonctionnaire",
    "Auto-entrepreneur",
    "Entrepreneur/Chef d'entreprise",
    "Profession libérale",
    "Consultant",
    "Freelance/Travailleur autonome",
    "Apprenti",
    "Contractuel",
    "Saisonnier",
    "Vacataire",
    "VSI (Volontaire de Solidarité Internationale)"
]


# 

# Job status to income tier mapping (Morocco-specific)
job_income_tiers = {
    # Low Income (MAD 0–3,000/month)
    "Stagiaire": "Low",
    "Saisonnier": "Low",
    "Apprenti": "Low",
    "Vacataire": "Low",
    "VSI (Volontaire de Solidarité Internationale)": "Low",
    
    # Medium Income (MAD 3,000–8,000/month)
    "Salarié": "Medium",
    "Fonctionnaire": "Medium",
    "Intérimaire": "Medium",
    "Contractuel": "Medium",
    "Auto-entrepreneur": "Medium",
    "Consultant": "Medium",
    "Freelance/Travailleur autonome": "Medium",
    
    # High Income (MAD 8,000+/month)
    "Entrepreneur/Chef d'entreprise": "High",
    "Profession libérale": "High",
}

# MCCs with Morocco-adjusted intervals (MAD)
mcc_intervals = {
    # Alimentation & Restaurants 🍔
    "5411": {"Category": "Épiceries/supermarchés", "Low": (50, 500), "Medium": (100, 1000), "High": (200, 2000)},
    "5812": {"Category": "Restaurants", "Low": (30, 300), "Medium": (50, 500), "High": (200, 1500)},
    "5813": {"Category": "Bars et discothèques", "Low": (50, 400), "Medium": (100, 800), "High": (300, 2500)},
    "5814": {"Category": "Fast-food", "Low": (20, 150), "Medium": (30, 300), "High": (50, 500)},
    
    # Transport & Voyages ✈️
    "4111": {"Category": "Transport en commun", "Low": (10, 100), "Medium": (20, 200), "High": (50, 500)},
    "4511": {"Category": "Compagnies aériennes", "Low": (0, 1000), "Medium": (1000, 5000), "High": (3000, 20000)},
    "4722": {"Category": "Agences de voyage", "Low": (100, 2000), "Medium": (500, 5000), "High": (2000, 15000)},
    "5541": {"Category": "Stations-service", "Low": (50, 300), "Medium": (100, 600), "High": (200, 1200)},
    
    # Santé & Médical 🏥
    "8011": {"Category": "Médecins", "Low": (100, 500), "Medium": (200, 1000), "High": (500, 3000)},
    "8062": {"Category": "Hôpitaux", "Low": (500, 3000), "Medium": (1000, 10000), "High": (5000, 50000)},
    
    # Achats & E-commerce 🛒
    "5732": {"Category": "Électronique", "Low": (500, 2000), "Medium": (1000, 10000), "High": (5000, 50000)},
    "5942": {"Category": "Librairies", "Low": (50, 300), "Medium": (100, 500), "High": (200, 1500)},
    
    # Services financiers 💰
    "6011": {"Category": "ATM", "Low": (200, 1000), "Medium": (500, 3000), "High": (1000, 10000)},
    "6300": {"Category": "Assurances", "Low": (100, 500), "Medium": (300, 1500), "High": (1000, 5000)},
}
