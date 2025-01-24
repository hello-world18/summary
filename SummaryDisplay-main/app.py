import os
import uuid
from datetime import datetime
from functools import wraps
import io
import base64
from io import BytesIO

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, send_file, send_from_directory
)
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import json 
import os
import uuid
from datetime import datetime
from functools import wraps
from io import BytesIO
from flask import Flask, render_template
from flask_mysqldb import MySQL
import csv
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment
from flask import send_file
from flask import Response
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, send_file, send_from_directory
)
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import json 

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = 'uploads'


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Akram@123'
app.config['MYSQL_DB'] = 'flask_auth_new'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

# Secret key for session management
app.secret_key = 'ohrcpehsfon'


# ********LIS DEPARTMENT WISE SUMMARY**********

def process_lis_dept_file(file2_path):
    try:
        df = pd.read_excel(file2_path, sheet_name='Test Based Investigation', skiprows=6)
        df.columns = df.columns.astype(str).str.strip()
        for col in ['Ordering Location', 'Visit Name', 'Sub Department Name']:
            df[col] = df[col].fillna('Unknown').astype(str).str.strip()
        
        sub_departments = ['Histopathology', 'Cytology', 'CLINICAL PATHOLOGY',
                          'HEMATOLOGY', 'Bio Chemistry', 'Microbiology']
        
        # Define required counts for each location(replace with actual required count values)
        required_counts = {
    'Histopathology': {
        'Dermatology': {'IP Required': 0, 'OP Required': 0},
        'General Medicine': {'IP Required': 0, 'OP Required': 0},
        'General Surgery': {'IP Required': 1, 'OP Required': 0},
        'Gynaecology And Obstetrics': {'IP Required': 1, 'OP Required': 0},
        'Orthopaedics': {'IP Required': 0, 'OP Required': 0},
        'Pediatrics': {'IP Required': 0, 'OP Required': 0},
        'Plastic Surgery': {'IP Required': 0, 'OP Required': 0},
        'Psychiatry': {'IP Required': 0, 'OP Required': 0},
        'Respiratory Medicine': {'IP Required': 0, 'OP Required': 0},
        'Urology': {'IP Required': 0, 'OP Required': 0}
    },
    'Cytology': {
        'Dermatology': {'IP Required': 0, 'OP Required': 0},
        'General Medicine': {'IP Required': 0, 'OP Required': 2},
        'General Surgery': {'IP Required': 0, 'OP Required': 2},
        'Gynaecology And Obstetrics': {'IP Required': 0, 'OP Required': 2},
        'Orthopaedics': {'IP Required': 0, 'OP Required': 2},
        'Pediatrics': {'IP Required': 0, 'OP Required': 1},
        'Plastic Surgery': {'IP Required': 0, 'OP Required': 0},
        'Psychiatry': {'IP Required': 0, 'OP Required': 0},
        'Respiratory Medicine': {'IP Required': 0, 'OP Required': 0},
        'Urology': {'IP Required': 0, 'OP Required': 1}
    },
    'CLINICAL PATHOLOGY': {
        'Dermatology': {'IP Required': 3, 'OP Required': 8},
        'General Medicine': {'IP Required': 23, 'OP Required': 20},
        'General Surgery': {'IP Required': 23, 'OP Required': 25},
        'Gynaecology And Obstetrics': {'IP Required': 15, 'OP Required': 25},
        'Orthopaedics': {'IP Required': 5, 'OP Required': 20},
        'Psychiatry': {'IP Required': 3, 'OP Required': 6},
        'Pediatrics': {'IP Required': 13, 'OP Required': 15},
        'Plastic Surgery': {'IP Required': 3, 'OP Required': 8},
        'Respiratory Medicine': {'IP Required': 3, 'OP Required': 8},
        'Urology': {'IP Required': 3, 'OP Required': 8}
    },
    'HEMATOLOGY': {
        'Dermatology': {'IP Required': 3, 'OP Required': 8},
        'General Medicine': {'IP Required': 23, 'OP Required': 20},
        'General Surgery': {'IP Required': 23, 'OP Required': 25},
        'Gynaecology And Obstetrics': {'IP Required': 15, 'OP Required': 25},
        'Orthopaedics': {'IP Required': 5, 'OP Required': 20},
        'Psychiatry': {'IP Required': 3, 'OP Required': 6},
        'Pediatrics': {'IP Required': 13, 'OP Required': 15},
        'Plastic Surgery': {'IP Required': 3, 'OP Required': 8},
        'Respiratory Medicine': {'IP Required': 3, 'OP Required': 8},
        'Urology': {'IP Required': 3, 'OP Required': 8}
    },
    'Bio Chemistry': {
        'Dermatology': {'IP Required': 3, 'OP Required': 8},
       'General Medicine': {'IP Required': 23, 'OP Required': 20},
        'General Surgery': {'IP Required': 23, 'OP Required': 25},
        'Gynaecology And Obstetrics': {'IP Required': 15, 'OP Required': 25},
        'Orthopaedics': {'IP Required': 5, 'OP Required': 20},
        'Pediatrics': {'IP Required': 13, 'OP Required': 15},
        'Plastic Surgery': {'IP Required': 3, 'OP Required': 8},
        'Psychiatry': {'IP Required': 3, 'OP Required':6},
        'Respiratory Medicine': {'IP Required': 3, 'OP Required': 8},
        'Urology': {'IP Required': 3, 'OP Required': 8}
    },
    'Microbiology': {
        'Dermatology': {'IP Required': 3, 'OP Required': 3},
        'General Medicine': {'IP Required': 23, 'OP Required': 6},
        'General Surgery': {'IP Required': 23, 'OP Required': 6},
        'Gynaecology And Obstetrics': {'IP Required': 15,'OP Required': 6},
        'Orthopaedics': {'IP Required': 5, 'OP Required': 6},
        'Pediatrics': {'IP Required': 13, 'OP Required': 5},
        'Plastic Surgery': {'IP Required': 3, 'OP Required': 3},
        'Psychiatry': {'IP Required': 3, 'OP Required': 3},
        'Respiratory Medicine': {'IP Required': 3, 'OP Required': 3},
        'Urology': {'IP Required': 3, 'OP Required': 4}
    }
}
        
        all_results = {}
        
        for dept in sub_departments:
            results, totals = process_lis_department_data(df, dept, required_counts)
            all_results[dept] = {'data': results, 'totals': totals}
        return all_results
    except Exception as e:
        return f'Error processing file: {str(e)}', 400


def process_lis_department_data(df, sub_dept, required_counts):
    base_locations = [
        'Dermatology', 'General Medicine', 'General Surgery',
        'Gynaecology And Obstetrics', 'Orthopaedics', 'Pediatrics',
        'Plastic Surgery', 'Psychiatry', 'Respiratory Medicine', 'Urology'
    ]
    visit_types = ['IP', 'OP', 'Emergency']
    df['Ordering Location'] = df['Ordering Location'].fillna('Unknown').astype(str)
    df['Normalized Location'] = df['Ordering Location'].apply(normalize_lis_location)
    
    results = []
    sl_no = 1
    
    for loc in base_locations:
        # Get required counts for this location and sub-department
        ip_required = required_counts.get(sub_dept, {}).get(loc, {}).get('IP Required', 0)
        op_required = required_counts.get(sub_dept, {}).get(loc, {}).get('OP Required', 0)
        
        row_data = {
            'Sl.No': sl_no,
            'Ordering Location': loc,
            'IP Required': ip_required,
            'OP Required': op_required
        }
        
        total_count = 0
        for visit in visit_types:
            count = len(df[
                (df['Normalized Location'] == loc) &
                (df['Visit Name'] == visit) &
                (df['Sub Department Name'] == sub_dept)
            ])
            row_data[visit] = count
            total_count += count
        
        row_data['Total'] = total_count
        results.append(row_data)
        sl_no += 1
    
    # Calculate totals
    totals = {'Sl.No': '', 'Ordering Location': 'Total'}
    total_sum = 0
    
    # Add required totals
    totals['IP Required'] = sum(row['IP Required'] for row in results)
    totals['OP Required'] = sum(row['OP Required'] for row in results)
    
    for visit in visit_types:
        visit_sum = sum(row[visit] for row in results)
        totals[visit] = visit_sum
        total_sum += visit_sum
    
    totals['Total'] = total_sum
    
    return results, totals


def normalize_lis_location(location):
    if pd.isna(location) or location is None:
        return "Unknown"
    location = str(location).strip()
    base_locations = [
        'Dermatology', 'General Medicine', 'General Surgery', 
        'Gynaecology And Obstetrics', 'Orthopaedics', 'Pediatrics', 
        'Plastic Surgery', 'Psychiatry', 'Respiratory Medicine', 'Urology'
    ]
    for base in base_locations:
        if location.startswith(base):
            return base
    return location


def generate_lis_visualizations(results):
    fig, ax = plt.subplots(figsize=(10, 6))
    locations = [row['Ordering Location'] for row in results]
    totals = [row['Total'] for row in results]

    sns.barplot(x=totals, y=locations, palette='coolwarm', ax=ax)
    ax.set_title('Total Visits by Department')
    ax.set_xlabel('Number of Visits')
    ax.set_ylabel('Departments')

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url
   
# ********LIS SUMMARY**********
FIXED_VALUES_BLANK1 = [0, 15, 100, 110, 210, 110]
FIXED_VALUES_BLANK2 = [15, 6, 75, 75, 160, 45]
patient_company = ["Aarogyasri", "EHS", "General", "Patient General"]
SUB_DEPARTMENTS = [
        'Histopathology',
        'Cytology',
        'HEMATOLOGY',
        'CLINICAL PATHOLOGY',
        'Bio Chemistry',
        'Microbiology'
    ]

def process_lis_file(lis_path):
    df_inv = pd.read_excel(lis_path,sheet_name='Test Based Investigation',header=6)
    
    if 'Patient Company ' not in df_inv.columns or 'Visit Name' not in df_inv.columns:
        return (
            "Required columns 'Patient Company' or 'Visit Name' not found in the file. "
            f"Found columns: {df_inv.columns.tolist()}",
            400,
        )
    df_inv_filtered_category = df_inv[df_inv['Sub Department Name'].isin(SUB_DEPARTMENTS) & df_inv['Patient Company '].isin(patient_company)]
    op_category_counts = (
            df_inv_filtered_category[df_inv_filtered_category['Visit Name'] == 'OP']
            .groupby('Patient Company ')
            .size()
            .reset_index(name='OP Patient Count')
        )
    ip_category_counts = (
           df_inv_filtered_category[df_inv_filtered_category['Visit Name'] == 'IP']
            .groupby('Patient Company ')
            .size()
            .reset_index(name='IP Patient Count')
        )
    
    summary_table1 = pd.DataFrame({
            'Patient Company ': patient_company
        })

    opd_category_table = pd.merge(
        summary_table1,
        op_category_counts,
        how='left',
        on='Patient Company '  
    )
    opd_category_table['OP Patient Count'] = opd_category_table['OP Patient Count'].fillna(0).astype(int)
   
    ipd_category_table = pd.merge(
        summary_table1,
        ip_category_counts,
        how='left',
        on='Patient Company '  
    )
    ipd_category_table['IP Patient Count'] = ipd_category_table['IP Patient Count'].fillna(0).astype(int)
    
    summary_table1 = pd.merge(
        summary_table1,
        op_category_counts,
        how='left',
        on='Patient Company '  
    )
    summary_table1 = pd.merge(
        summary_table1,
        ip_category_counts,
        how='left',
        on='Patient Company '  
    )
   
    summary_table1['IP Patient Count'] = summary_table1['IP Patient Count'].fillna(0).astype(int)
    summary_table1['OP Patient Count'] = summary_table1['OP Patient Count'].fillna(0).astype(int)
    total_row1 = {
            'Patient Company ': 'Total',
            'OP Patient Count': summary_table1['OP Patient Count'].sum(),
            'IP Patient Count': summary_table1['IP Patient Count'].sum(),
        }
    summary_table1 = pd.concat([summary_table1, pd.DataFrame([total_row1])], ignore_index=True)
    summary_html_categories = summary_table1.to_html(
                index=False,
                classes='table table-bordered',
                border=0,
                justify='center'
            )
    
    results_lis = process_lis_excel(lis_path)
    return ( results_lis,summary_html_categories,opd_category_table,ipd_category_table)

def process_lis_excel(lis_path):
    try:
        
        main_df = pd.read_excel(lis_path, skiprows=6)
        detail_df = pd.read_excel(lis_path, sheet_name='Deatil Investigation Report', skiprows=2)

        results = []

        for i, dept in enumerate(SUB_DEPARTMENTS):

            dept_data = main_df[main_df['Sub Department Name'] == dept]
            ip_count = len(dept_data[dept_data['Visit Name'] == 'IP'])
            
            op_count = len(dept_data[dept_data['Visit Name'] == 'OP'])
            dispatch_count = get_dispatch_count(detail_df, dept)
            total_count = op_count + ip_count
            formatted_dept = dept.capitalize()

            
            op_patients = dept_data[dept_data['Visit Name'] == 'OP'].to_dict(orient='records')
            ip_patients = dept_data[dept_data['Visit Name'] == 'IP'].to_dict(orient='records')

            # Assuming 'Dispatch Count' corresponds to patient details in 'detail_df'
            dispatch_patients = detail_df[
                (detail_df['Dept. Name'].str.lower() == dept) & 
                (detail_df['Status'] == 'dispatched')
            ].to_dict(orient='records')
           
            results.append({
                'sl_no': i + 1,
                'sub_department': formatted_dept,
                'blank1': FIXED_VALUES_BLANK1[i],
                'blank2': FIXED_VALUES_BLANK2[i],
                'op_count': op_count,
                'ip_count': ip_count,
                'dispatch_count': dispatch_count,
                'total_count': total_count,
                'op_patients': op_patients,
                'ip_patients': ip_patients,
                'dispatch_patients': dispatch_patients,
            })

        
        total_blank1 = sum(FIXED_VALUES_BLANK1)
        total_blank2 = sum(FIXED_VALUES_BLANK2)
        total_op_count = sum(item['op_count'] for item in results)
        total_ip_count = sum(item['ip_count'] for item in results)
        total_dispatch_count = sum(item['dispatch_count'] for item in results)
        total_total_count = total_op_count + total_ip_count
        
        results.append({
            'sl_no': '',
            'sub_department': 'Total',
            'blank1': total_blank1,
            'blank2': total_blank2,
            'op_count': total_op_count,
            'ip_count': total_ip_count,
            'dispatch_count': total_dispatch_count,
            'total_count': total_total_count,
            'op_patients': [],
            'ip_patients': [],
            'dispatch_patients': [],
        })

        return results

    except Exception as e:
        raise Exception(f"Error processing the Excel file: {e}")

def get_dispatch_count(detail_df, department):
    """
    Extracts dispatch count from the Detail Investigation Report sheet.

    Args:
        detail_df (pandas.DataFrame): The DataFrame containing detail investigation report data.
        department (str): The department name.

    Returns:
        int: The number of dispatches for the given department.

    Raises:
        KeyError: If 'Status' or 'Dept. Name' columns are missing in the DataFrame.
    """

    detail_df.columns = detail_df.columns.str.strip()
    
    if 'Status' not in detail_df.columns or 'Dept. Name' not in detail_df.columns:
        raise KeyError("Missing 'Status' or 'Dept. Name' column in the Detail Investigation Report sheet.")

    detail_df['Status'] = detail_df['Status'].str.strip().str.lower()
    dept_data = detail_df[
        (detail_df['Dept. Name'] == department) &
        (detail_df['Status'] == 'dispatched')
    ]

    return len(dept_data)

# ********RIS SUMMARY**********
def process_ris_excel(file7_path):
    import pandas as pd
    
    # Read Excel file starting from row 8 (0-based index is 7)
    df = pd.read_excel(file7_path, skiprows=7)
    
    # Fill NaN values in relevant columns with empty strings
    df['Ordering Location'] = df['Ordering Location'].fillna('')
    df['Visit Type'] = df['Visit Type'].fillna('')
    df['Sub Department'] = df['Sub Department'].fillna('')
    df['Patient Company'] = df['Patient Company'].fillna('')
    
    # Define main department categories
    main_departments = [
        'Dermatology',
        'General Medicine',
        'General Surgery',
        'Gynaecology And Obstetrics',
        'Orthopaedics',
        'Pediatrics',
        'Plastic Surgery',
        'Psychiatry',
        'Respiratory Medicine',
        'Urology'
    ]
    
    # Define allowed Patient Company values
    allowed_companies = ['General', 'Aarogyasri', 'EHS', 'Patient General']
    
    # Filter data for allowed Patient Company values
    company_filtered_df = df[df['Patient Company'].isin(allowed_companies)]
    company_filtered_df_category_ris=company_filtered_df

    # Initialize results dictionaries with zeros for all departments
    visit_type_results = {dept: {
        'IP': 0,
        'OP': 0,
        'Emergency': 0,
        'Total': 0
    } for dept in main_departments}
    
    modality_results = {dept: {
        'XRAY': 0,
        'CT Scan': 0,
        'Ultra Sound': 0,
        'MRI': 0,
        'Total': 0
    } for dept in main_departments}
    
    # Process data for both tables
    for dept in main_departments:
        # Filter locations that begin with the department name
        dept_mask = company_filtered_df['Ordering Location'].str.startswith(dept, na=False)
        if dept_mask.any():  # Check if there are any matching records
            location_data = company_filtered_df[dept_mask]
            
            # Visit Type counts
            visit_type_results[dept] = {
                'IP': len(location_data[location_data['Visit Type'] == 'IP']),
                'OP': len(location_data[location_data['Visit Type'] == 'OP']),
                'Emergency': len(location_data[location_data['Visit Type'] == 'Emergency']),
                'Total': len(location_data)
            }
            
            # Modality counts
            modality_results[dept] = {
                'XRAY': len(location_data[location_data['Sub Department'] == 'XRAY']),
                'CT Scan': len(location_data[location_data['Sub Department'] == 'CT Scan']),
                'Ultra Sound': len(location_data[location_data['Sub Department'] == 'Ultra Sound']),
                'MRI': len(location_data[location_data['Sub Department'] == 'MRI']),
                'Total': len(location_data)
            }
            
          
            
    
    
    # Second Table: Patient Category Summary
    # patient_category = ['General', 'Aarogyasri', 'EHS', 'Patient General']
    if 'Patient Company' not in company_filtered_df_category_ris or 'Visit Type' not in company_filtered_df_category_ris:
        return (
                "Required columns 'Patient Company' or 'Visit Type' not found in the file. "
                f"Found columns: {company_filtered_df_category_ris.columns.tolist()}",
                400,
                )

   
    df_filtered_category = company_filtered_df_category_ris[company_filtered_df_category_ris['Ordering Location'].str.startswith(tuple(main_departments), na=False)]

    op_category_counts = (
            df_filtered_category[df_filtered_category['Visit Type'] == 'OP']
            .groupby('Patient Company')
            .size()
            .reset_index(name='OP Patient Count')
        )
    ip_category_counts = (
           df_filtered_category[df_filtered_category['Visit Type'] == 'IP']
            .groupby('Patient Company')
            .size()
            .reset_index(name='IP Patient Count')
        )
    
    
    summary_table_ris = pd.DataFrame({
                'Patient Company': allowed_companies
            })
    
    opd_category_table = pd.merge(
        summary_table_ris,
        op_category_counts,
        how='left',
        on='Patient Company'  
    )
    opd_category_table['OP Patient Count'] = opd_category_table['OP Patient Count'].fillna(0).astype(int)
   
    ipd_category_table = pd.merge(
        summary_table_ris,
        ip_category_counts,
        how='left',
        on='Patient Company'  
    )
    
    ipd_category_table['IP Patient Count'] = ipd_category_table['IP Patient Count'].fillna(0).astype(int)
    
    summary_table_ris = pd.merge(
        summary_table_ris,
        op_category_counts,
        how='left',
        on='Patient Company'  
    )
    summary_table_ris = pd.merge(
        summary_table_ris,
        ip_category_counts,
        how='left',
        on='Patient Company'  
    )
    
    summary_table_ris['IP Patient Count'] = summary_table_ris['IP Patient Count'].fillna(0).astype(int)
    summary_table_ris['OP Patient Count'] = summary_table_ris['OP Patient Count'].fillna(0).astype(int)
    total_row1 = {
            'Patient Company': 'Total',
            'OP Patient Count': summary_table_ris['OP Patient Count'].sum(),
            'IP Patient Count': summary_table_ris['IP Patient Count'].sum(),
        }
    summary_table_ris = pd.concat([summary_table_ris, pd.DataFrame([total_row1])], ignore_index=True)
    
    summary_html_categories = summary_table_ris.to_html(
                index=False,
                classes='table table-bordered',
                border=0,
                justify='center'
            )
    

    return visit_type_results, modality_results,summary_html_categories
  
# ********Doctors SUMMARY**********
def process_doctors_file(file1_path):
    # Read Excel file starting from row 8 (0-based index is 7)
    df = pd.read_excel(file1_path, skiprows=7)
    
    # Initialize results dictionary
    results = []
    
    # Get unique departments
    departments = df['Department'].unique()
    
    # Counter for serial number
    sl_no = 1
    
    # Process each department
    for dept in departments:
        # Filter by department and IP visits
        dept_df = df[
            (df['Department'] == dept) & 
            (df['Visit Type'] == 'IP')
        ]
        
        # Group by Consulting Doctor and get counts
        doctor_counts = dept_df['Consulting Doctor'].value_counts()
        
        # Add each doctor's count to results
        for doctor, count in doctor_counts.items():
            results.append({
                'Sl.No': sl_no,
                'Department': dept,
                'Consulting Doctor': doctor,
                'Total Count': count
            })
            sl_no += 1
    
    # Convert results to DataFrame
    results_dr = pd.DataFrame(results)
    
    # Calculate total
    total_count_dr = results_dr['Total Count'].sum()
    
    return results_dr, total_count_dr

# ********OT SUMMARY**********
def process_ot_file(ot_path):
     # Read Excel file starting from row 8 (0-based index is 7)
    df = pd.read_excel(ot_path, skiprows=7)
   
    # Initialize results dictionary
    departments = ['General Surgery', 'Orthopaedics', 'Gynaecology And Obstetrics', 'Plastic Surgery', 'Urology']
    results_minor = []
    results_major=[]
    results=[]
    for idx, dept in enumerate(departments, 1):
       
    
        minor_patient_general = df[
            (df['Operation Type'] == 'MINOR OPERATIONS') & 
            (df['Department Name'].str.startswith(dept)) & 
            (df['Patient Category'] == 'Patient General')
        ].shape[0]
        major_patient_general = df[
            (df['Operation Type'] == 'MAJOR OPERATIONS') & 
            (df['Department Name'].str.startswith(dept)) & 
            (df['Patient Category'] == 'Patient General')
        ].shape[0]
        # minor fixed values
        FIXED_VALUES_BLANK1 = [6, 6, 6, 6, 6, 6]
        # major fixed values
        FIXED_VALUES_BLANK2 = [3, 3, 3, 3, 3, 3]
        # Sum up counts for all three categories
            # Count for Aarogyasri
        major_arg = df[
                (df['Operation Type'] == 'MAJOR OPERATIONS') & 
                (df['Department Name'].str.startswith(dept)) & 
                (df['Patient Category'] == 'Aarogyasri')
            ].shape[0] 
            # Count for General
        major_gen = df[
                (df['Operation Type'] == 'MAJOR OPERATIONS') & 
                (df['Department Name'].str.startswith(dept)) & 
                (df['Patient Category'] == 'General')
            ].shape[0] 
            # Count for ESH
        major_esh =    df[
                (df['Operation Type'] == 'MAJOR OPERATIONS') & 
                (df['Department Name'].str.startswith(dept)) & 
                (df['Patient Category'] == 'ESH')
            ].shape[0]
        
           # Count for Aarogyasri
        minor_arg = df[
                (df['Operation Type'] == 'MINOR OPERATIONS') & 
                (df['Department Name'].str.startswith(dept)) & 
                (df['Patient Category'] == 'Aarogyasri')
            ].shape[0] 
            # Count for General
        minor_gen = df[
                (df['Operation Type'] == 'MINOR OPERATIONS') & 
                (df['Department Name'].str.startswith(dept)) & 
                (df['Patient Category'] == 'General')
            ].shape[0] 
            # Count for ESH
        minor_esh =    df[
                (df['Operation Type'] == 'MINOR OPERATIONS') & 
                (df['Department Name'].str.startswith(dept)) & 
                (df['Patient Category'] == 'ESH')
            ].shape[0]
        minor_total = minor_patient_general + minor_gen + minor_arg + minor_esh
        major_total = major_patient_general + major_gen + major_arg + major_esh
        results_major.append({
            'sl_no': idx,
            'department': dept,
            'blank2': FIXED_VALUES_BLANK2[idx],
            'major_patient_general': major_patient_general,
            'major_gen': major_gen,
            'major_arg' : major_arg,
            'major_esh' : major_esh,
            'major_total': major_total,    
        })
        results_minor.append({
            'sl_no': idx,
            'department': dept,
            'blank1': FIXED_VALUES_BLANK1[idx],
            'minor_patient_general': minor_patient_general,
            'minor_gen': minor_gen,
            'minor_arg' : minor_arg,
            'minor_esh' : minor_esh,
            'minor_total': minor_total,   
        })
    # Calculate totals
    totals_minor = {
        'sl_no': '',
        'department': 'Total',
        'blank1': sum(r['blank1'] for r in results_minor),
        'minor_patient_general': sum(r['minor_patient_general'] for r in results_minor),
        'minor_gen': sum(r['minor_gen'] for r in results_minor),
        'minor_arg': sum(r['minor_arg'] for r in results_minor),
        'minor_esh': sum(r['minor_esh'] for r in results_minor),
        'minor_total': sum(r['minor_total'] for r in results_minor),
    }
    totals_major = {
        'sl_no': '',
        'department': 'Total',
        'blank2': sum(r['blank2'] for r in results_major),
        'major_patient_general': sum(r['major_patient_general'] for r in results_major),
        'major_gen': sum(r['major_gen'] for r in results_major),
        'major_arg': sum(r['major_arg'] for r in results_major),
        'major_esh': sum(r['major_esh'] for r in results_major),
        'major_total': sum(r['major_total'] for r in results_major),
    }
    
    results_minor.append(totals_minor)
    results_major.append(totals_major)
    results.append(results_major)
    results.append(results_minor)

    return results

# ********Biopsy SUMMARY**********
def process_biopsy_file(biopsy_path):
    # Read Excel file starting from row 8 (0-based index is 7)
    df = pd.read_excel(biopsy_path, skiprows=7)
    
    # Initialize results list
    results = []
    departments = ['General Surgery', 'Orthopaedics', 'Gynaecology And Obstetrics', 'Plastic Surgery', 'Urology']
    
    # Counter for serial number
    sl_no = 1
    total_count = 0
    
    # Process each department
    for dept in departments:
        # Filter by department and HEMATOLOGY
        dept_data = df[
            (df['Department'] == dept) & 
            (df['Sub Department'] == 'Histopathology')
        ]
       
        # Get IP count
        ip_count = dept_data['IP'].sum()
        
        total_count += ip_count
        
        # Add to results if there are any records
        if not dept_data.empty:
            results.append({
                'sl_no': sl_no,
                'department': dept,
                'ip_count': int(ip_count)
            })
            sl_no += 1
    
    # Add total row
    results.append({
        'sl_no': '',
        'department': 'Total',
        'ip_count': int(total_count)
    })
    
    return results

# ********OPD SUMMARY**********
def process_opd_file(file1_path,file_date_str,file_id):
    df = pd.read_excel(file1_path, header=7)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, opd_required FROM departments")
    departments_data = cursor.fetchall()
    cursor.close()
    
    # Convert the database rows into separate lists for departments and OPD Required values
    departments = [str(row[0]).strip() for row in departments_data] 
    opd_required = [row[1] for row in departments_data]
    if 'Department' not in df.columns or 'Visit Type' not in df.columns:
        return (
                "Required columns 'Department' or 'Visit Type' not found in the file. "
                f"Found columns: {df.columns.tolist()}",
                400,
                )
    df_filtered = df[df['Department'].isin(departments)]
    opd_counts = (
                df_filtered[df_filtered['Visit Type'] == 'OP']
                .groupby('Department')
                .size()
                .fillna(0)
                .reset_index(name='Daily OPD Count')
            )
    
    # Modify the OPD counts DataFrame to include hyperlinks
    opd_counts['Daily OPD Count'] = opd_counts.apply(
            lambda row: f'<a style="text-decoration: none; cursor: pointer; color:black" href="/department_details/{row["Department"]}/{file_id}" target="_blank">{row["Daily OPD Count"]}</a>',
            axis=1
            )
    # print(opd_counts['Daily OPD Count'])
    summary_table = pd.DataFrame({
            'Sl.No': range(1, len(departments) + 1),
            'Departments': departments,
            'OPD Required': opd_required,
            })
        
    summary_table = pd.merge(
            summary_table,
            opd_counts,
            left_on='Departments',
            right_on='Department',
            how='left'
        )
    
    # print(summary_table['Daily OPD Count'])
     # Extract numeric values from the HTML strings
    
    summary_table['Daily OPD Count num'] = summary_table['Daily OPD Count'].str.extract(r'>(\d+)<').fillna(0).astype(int)
    
    
    # Calculate the sum of the numeric column
    total_today_opd = summary_table['Daily OPD Count num'].sum()
    summary_table.drop(columns=['Department'], inplace=True)
    summary_table.drop(columns=['Daily OPD Count num'], inplace=True)
    
    # Create the total value as a link
    total_today_opd_link = f'<a style="text-decoration: none; cursor: pointer; color:black" href="/preview/{file_id}" target="_blank">{total_today_opd}</a>'   
     
    total_row = {
            'Sl.No': '',
            'Departments': 'Total',
            'OPD Required': summary_table['OPD Required'].sum(),
            'Daily OPD Count': total_today_opd_link,
        }
          
    summary_table = pd.concat([summary_table, pd.DataFrame([total_row])], ignore_index=True)
    
    summary_html_departments = summary_table.to_html(
            index=False,
            classes='table table-bordered',
            border=0,
            justify='center',
            escape=False  # Allow rendering HTML in table cells
        )
    
    # Second Table: Patient Category Summary
    patient_category = ["Aarogyasri", "ESH", "General", "Patient General"]
    if 'Patient Category' not in df.columns or 'Visit Type' not in df.columns:
        return (
                "Required columns 'Patient Category' or 'Visit Type' not found in the file. "
                f"Found columns: {df.columns.tolist()}",
                400,
                )

    df_filtered_category = df[df['Department'].isin(departments) & df['Patient Category'].isin(patient_category)]
    category_counts = (
        df_filtered_category[df_filtered_category['Visit Type'] == 'OP']
            .groupby('Patient Category')
            .size()
            .reset_index(name='Patient Count')
            )
    
    summary_table1 = pd.DataFrame({
                'Patient Category': patient_category
            })
    summary_table1 = pd.merge(
                summary_table1,
                category_counts,
                left_on='Patient Category',
                right_on='Patient Category',
                how='left'
            )
    summary_table1['Patient Count'] = summary_table1['Patient Count'].fillna(0).astype(int)
    total_row1 = {
                'Patient Category': 'Total',
                'Patient Count': summary_table1['Patient Count'].sum(),
            }
    summary_table1 = pd.concat([summary_table1, pd.DataFrame([total_row1])], ignore_index=True)
    summary_table1['Patient Category'] = summary_table1['Patient Category'].replace('ESH', 'EHS')
    summary_html_categories = summary_table1.to_html(
                index=False,
                classes='table table-bordered',
                border=0,
                justify='center'
            )

    return summary_html_departments,summary_html_categories,summary_table,summary_table1
            
# ********IPD SUMMARY**********

# Helper functions to filter and process the data
def filter_daily_patient_list(df):
    departments = ['Dermatology', 'General Medicine', 'General Surgery',
                   'Gynaecology And Obstetrics', 'Orthopaedics',
                   'Pediatrics', 'Plastic Surgery', 'Psychiatry',
                   'Respiratory Medicine', 'Urology']
    results = []
    for department in departments:
        filtered_data = df[(df['Department'] == department) & (df['Visit Type'] == 'IP')]
        count_general = filtered_data[filtered_data['Patient Category'] == 'Patient General'].shape[0]
        count_aes = filtered_data[filtered_data['Patient Category'].isin(['Aarogyasri', 'General', 'ESH'])].shape[0]
        results.append({
            'Department': department,
            'Count (Patient General)': count_general,
            "Count ('Aarogyasri + General + ESH')": count_aes,
        })
    return results

def filter_daily_patient_doctor_list(df):
    doctors = {
        'General Medicine': ['Dr. ABU BAKER', 'Dr. SUHAIL BIN AHMED'],
        'General Surgery': ['Dr. GANESH R PRASAD', 'Dr. A HADI']
    }
    results = []
    for department, doctor_list in doctors.items():
        for doctor in doctor_list:
            filtered_data = df[(df['Department'] == department) & (df['Visit Type'] == 'IP') & (df['Consulting Doctor'].str.contains(doctor))]
            count_general = filtered_data[filtered_data['Patient Category'] == 'Patient General'].shape[0]
            count_aes = filtered_data[filtered_data['Patient Category'].isin(['Aarogyasri', 'General', 'ESH'])].shape[0]
            results.append({
                'Department': department,
                'Doctor': doctor,
                'Count (Patient General)': count_general,
                "Count ('Aarogyasri + General + ESH')": count_aes,
            })
    return results

def filter_ipd_patient_list(df):
    departments = ['Dermatology', 'General Medicine', 'General Surgery', 'Gynaecology And Obstetrics', 
                   'Orthopaedics', 'Pediatrics', 'Plastic Surgery', 'Psychiatry', 'Respiratory Medicine', 'Urology']
    results = []
    for department in departments:
        filtered_data = df[(df['Department of Consultant'] == department)]
        discharge_count = filtered_data.shape[0] if not filtered_data.empty else 0
        results.append({
            'Department': department,
            'Discharge Count': discharge_count,
        })
    return results

def filter_bed_occupancy(df):
    departments = ['Dermatology', 'General Medicine', 'General Surgery', 'Gynaecology And Obstetrics', 
                   'Orthopaedics', 'Pediatrics', 'Plastic Surgery', 'Psychiatry', 'Respiratory Medicine', 'Urology']
    bed_counts = {}
    for department in departments:
        count = df[df['Current Department'] == department].shape[0]
        bed_counts[department] = count
    return bed_counts

# Create the final reports for all departments and doctors
def create_report(opd_counts, discharge_counts, bed_counts):
    report_data = []
    FIXED_VALUES_BLANK3 = [9,48,48,24,16,20,13,12,16,13]
    for i, opd in enumerate(opd_counts, start=0):
        department = opd['Department']
        patient_on_bed = bed_counts.get(department, 0)
        discharge_count = next((item['Discharge Count'] for item in discharge_counts if item['Department'] == department), 0)
        total_count = opd['Count (Patient General)'] + opd["Count ('Aarogyasri + General + ESH')"]
        report_data.append({
            'Sl. No': i+1,
            'Department': department,
            'IPD 80 %': FIXED_VALUES_BLANK3[i],
            'Patient on Bed': patient_on_bed,
            "Count (Patient General)": opd['Count (Patient General)'],
            "Count ('Aarogyasri + General + ESH')": opd["Count ('Aarogyasri + General + ESH')"],
            'Discharge Count': discharge_count,
            'Day Count': total_count,
        })
    return pd.DataFrame(report_data)


def process_ipd_file(file1_path,file5_path,file6_path):
    # Read Excel files
    daily_patient_df = pd.read_excel(file1_path, skiprows=7)
    ipd_patient_df = pd.read_excel(file6_path, skiprows=3)
    bed_occupancy_df = pd.read_excel(file5_path)
    # Clean DataFrames by dropping empty rows and resetting index
    daily_patient_df.dropna(how='all', inplace=True)
    ipd_patient_df.dropna(how='all', inplace=True)
    bed_occupancy_df.dropna(how='all', inplace=True)

    daily_patient_df.reset_index(drop=True, inplace=True)
    ipd_patient_df.reset_index(drop=True, inplace=True)
    bed_occupancy_df.reset_index(drop=True, inplace=True)
    
    # Extract and process data for reports
    opd_counts = filter_daily_patient_list(daily_patient_df)
    opd_doctor_counts = filter_daily_patient_doctor_list(daily_patient_df)
    discharge_counts = filter_ipd_patient_list(ipd_patient_df)
    bed_counts = filter_bed_occupancy(bed_occupancy_df)
    
     # Create reports for all departments and doctors
    report_df_all_departments = create_report(opd_counts, discharge_counts, bed_counts)
    
   
    
    total_row = {
                'Sl. No':'',
                'Department': 'Total',
                'IPD 80 %': report_df_all_departments['IPD 80 %'].sum(),
                'Patient on Bed': report_df_all_departments['Patient on Bed'].sum(),
                'Count (Patient General)': report_df_all_departments['Count (Patient General)'].sum(),
                "Count ('Aarogyasri + General + ESH')": report_df_all_departments["Count ('Aarogyasri + General + ESH')"].sum(),
                'Discharge Count': report_df_all_departments['Discharge Count'].sum(),
                'Day Count': report_df_all_departments['Day Count'].sum(),
            }
    report_df_all_departments = pd.concat([report_df_all_departments, pd.DataFrame([total_row])], ignore_index=True)
    department_names = report_df_all_departments['Department'].tolist()
    ipd80Percent = report_df_all_departments['IPD 80 %'].tolist()
    totalCounts = report_df_all_departments['Day Count'].tolist()
    PatientGeneral= report_df_all_departments["Count (Patient General)"].tolist()
    General=report_df_all_departments["Count ('Aarogyasri + General + ESH')"].tolist()

    
    tables_ipd = [
    report_df_all_departments.to_html(classes='data', header="true", index=False).replace("\n", "").replace("]", ""),
    ]

   
    return tables_ipd,totalCounts,ipd80Percent,department_names,PatientGeneral,General
# Authorization decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Role-based access decorator
def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != role:
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# Routes
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()  # Fetch the user record
        cursor.close()

        if user:
            # `user` contains the following:
            # user[0] -> id, user[1] -> username, user[2] -> hashed_password, user[3] -> role
            hashed_password = user[2]

            # Validate the password using bcrypt
            if bcrypt.check_password_hash(hashed_password, password):
                # Password matches; set session variables
                session['logged_in'] = True
                session['username'] = user[1]
                session['role'] = user[3]

                # Insert login record into user_sessions table
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO user_sessions (user_id, login_time) VALUES (%s, NOW())", (user[0],))
                mysql.connection.commit()
                cursor.close()

                flash(f'Welcome, {user[1]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                # Invalid password
                flash('Invalid username or password.', 'danger')
        else:
            # User not found
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin():
    if request.method == 'POST':
        # Add a new user
        new_username = request.form['username']
        new_password = request.form['password']
        new_role = request.form['role']

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (new_username, hashed_password, new_role)
            )
            mysql.connection.commit()
            flash(f'User {new_username} added successfully!', 'success')
        except Exception as e:
            flash('Error adding user. Username might already exist.', 'danger')
        finally:
            cursor.close()

    # Fetch all users
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    cursor.close()
    return render_template('admin.html', username=session['username'], users=users)@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def update_user(user_id):
    if request.method == 'POST':
        updated_username = request.form['username']
        updated_password = request.form['password']
        updated_role = request.form['role']

        hashed_password = bcrypt.generate_password_hash(updated_password).decode('utf-8')

        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                "UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s",
                (updated_username, hashed_password, updated_role, user_id)
            )
            mysql.connection.commit()
            flash('User updated successfully.', 'success')
        except Exception as e:
            flash('Error updating user.', 'danger')
        finally:
            cursor.close()

        return redirect(url_for('admin'))

    # Fetch the user details to pre-fill the update form
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        flash('Error deleting user.', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('admin'))

@app.route('/departments', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def departments():
    if request.method == 'POST':
        # Add a new departmet
        new_department = request.form['name']
        new_opdRequired = request.form['opd_required']

        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO departments (name,opd_required) VALUES (%s, %s)",
                 (new_department, new_opdRequired)
            )
            mysql.connection.commit()
            flash(f'{new_department} added successfully!', 'success')
        except Exception as e:
            flash('Error adding department. Department might already exist.', 'danger')
        finally:
            cursor.close()
            
    # fetch all departments      
    cursor = mysql.connection.cursor()      
    cursor.execute("SELECT id, name, opd_required FROM departments")
    departments = cursor.fetchall()
    

    return render_template('departments.html', username=session['username'],departments=departments)

@app.route('/edit_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_department(department_id):
    if request.method == 'POST':
        # Fetch updated values from the form
        updated_name = request.form.get('name')
        updated_opd_required = request.form.get('opd_required')

        if not updated_name or not updated_opd_required:
            flash("Both Department Name and OPD Required are mandatory.", "danger")
            return redirect(url_for('edit_department', department_id=department_id))

        try:
            updated_opd_required = int(updated_opd_required)  # Convert OPD required to integer
        except ValueError:
            flash("OPD Required must be a number.", "danger")
            return redirect(url_for('edit_department', department_id=department_id))

        # Update the department in the database
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                "UPDATE departments SET name = %s, opd_required = %s WHERE id = %s",
                (updated_name, updated_opd_required, department_id)
            )
            mysql.connection.commit()
            flash("Department updated successfully.", "success")
        except Exception as e:
            flash(f"Error updating department: {str(e)}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('departments'))

    # Handle GET request to fetch department details
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id, name, opd_required FROM departments WHERE id = %s", (department_id,))
        department = cursor.fetchone()

        if department is None:
            flash("Department not found.", "danger")
            return redirect(url_for('departments'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('departments'))
    finally:
        cursor.close()

    # Render the edit department form
    return render_template('edit_department.html', department=department)

@app.route('/delete_department/<int:department_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_department(department_id):
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM departments WHERE id = %s", (department_id,))
        mysql.connection.commit()
        cursor.close()
        flash("Department deleted successfully")
    except Exception as e:
        flash('Error deleting user.', 'danger')
    finally:
        if cursor:
            cursor.close()  
        
    return redirect(url_for('departments'))

@app.route('/upload', methods=['POST'])
@login_required
@role_required('admin')
def upload_file():
    
    if 'visitRegister' not in request.files or 'IpdDischarge' not in request.files or 'BedOccupancy' not in request.files or 'LISTestRegister' not in request.files or 'OTRegister' not in request.files or 'DWSReport' not in request.files or 'RISRegister' not in request.files:
        flash('No file selected.', 'upload_error')
        return redirect(url_for('dashboard'))

    date = request.form['date']
    file = request.files['visitRegister']
    bedOccupancy = request.files['BedOccupancy']
    ipdDischarge = request.files['IpdDischarge']
    lis = request.files['LISTestRegister']
    ot = request.files['OTRegister']
    biopsy = request.files['DWSReport']
    ris = request.files['RISRegister']
    
    if (lis and ot) and (biopsy and file) and (bedOccupancy and ipdDischarge) and ris:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        bedOccupancy_path = os.path.join(app.config['UPLOAD_FOLDER'], bedOccupancy.filename)
        ipdDischarge_path = os.path.join(app.config['UPLOAD_FOLDER'], ipdDischarge.filename)
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        lis_path = os.path.join(app.config['UPLOAD_FOLDER'], lis.filename)
        ot_path = os.path.join(app.config['UPLOAD_FOLDER'], ot.filename)
        biopsy_path = os.path.join(app.config['UPLOAD_FOLDER'], biopsy.filename)
        ris_path = os.path.join(app.config['UPLOAD_FOLDER'], ris.filename)
        
        file.save(filepath)
        bedOccupancy.save(bedOccupancy_path)
        ipdDischarge.save(ipdDischarge_path)
        lis.save(lis_path)
        ot.save(ot_path)
        biopsy.save(biopsy_path)
        ris.save(ris_path) 
           
        # # RECEIVE VALUE for lis
        # results_lis,summary_html_categories = process_lis_file(lis_path)
        # # sends results in frontend required results and date time
        # results_ot = process_ot_file(ot_path) 
        # # biopsy
        # results_biopsy = process_biopsy_file(biopsy_path) 
        # Insert into the database
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
            "INSERT INTO files (file1_path, file2_path, file3_path, file4_path,file5_path, file6_path,file7_path ,date) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
            (filepath, lis_path, ot_path, biopsy_path,bedOccupancy_path,ipdDischarge_path,ris_path, date)
            )
            
            mysql.connection.commit()
            flash(f'Files uploaded successfully.', 'upload_success')
        except Exception as e:
            flash(f'Error saving file info: {e}', 'upload_error')
        finally:
            cursor.close()
        return redirect(url_for('dashboard'))
   
@app.route('/retrieve', methods=['GET'])
@login_required
def retrieve_files():
    date = request.args.get('date')
    file_date_obj = datetime.strptime(date, "%Y-%m-%d")
    file_date_str = file_date_obj.strftime("%d-%m-%Y")
    
    cursor = mysql.connection.cursor()
    cursor.execute(
    "SELECT id, file1_path, file2_path, file3_path, file4_path,file5_path, file6_path,file7_path, date FROM files WHERE date = %s", 
    (date,)
    )
    files = cursor.fetchall()
    cursor.close()

    if not files:
        flash('No files found for the selected date.', 'retrieve_error')
        return redirect(url_for('dashboard'))

    flash('Files retrieved successfully.', 'retrieve_success')
    return render_template('dashboard.html', files=files, search_date=file_date_str, username=session['username'], role=session['role'])

@app.route('/summary/<int:file_id>', methods=['GET'])
@login_required
def summarize_file(file_id):
  
    
    
    
    
    # Fetch file path and date from the database
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT file1_path, file2_path, file3_path, file4_path,file5_path, file6_path,file7_path, date FROM files WHERE id = %s", 
        (file_id,)
    )
    file = cursor.fetchall()
    cursor.close()
    
    if file:
        # Extract file paths and date
        file1_path, file2_path, file3_path, file4_path,file5_path, file6_path,file7_path, file_date = file[0]
        file_date_str = file_date.strftime("%d-%m-%Y")  # Format the date as YYYY-MM-DD
        
        # Check if all files exist at their specified paths
        missing_files = []
        for file_path in [file1_path, file2_path, file3_path, file4_path,file5_path, file6_path,file7_path,]:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            # If any file is missing, return a 404 response with the list of missing file paths
            return f"The following files were not found: {', '.join(missing_files)}", 404

        try:
            
            #summary_html_departments,summary_html_categories
            summary_html_departments,summary_html_categories,summary_table,summary_table1=process_opd_file(file1_path,file_date_str,file_id)
            # IPD
            
            tables,totalCounts,ipd80Percent,department_names,PatientGeneral,General = process_ipd_file(file1_path,file5_path,file6_path)
            # RECEIVE VALUE for lis
            
            results_lis,summary_html_categories_lis,opd_category_table,ipd_category_table = process_lis_file(file2_path)
            # RECEIVE VALUE for lis department wise
            all_results_lis=process_lis_dept_file(file2_path)
            
            
            # sends results in frontend required results and date time
            results_ot = process_ot_file(file3_path) 
            # biopsy
            results_biopsy = process_biopsy_file(file4_path) 
            # Doctor wise
            results_dr, total_count_dr = process_doctors_file(file1_path)   
            # Ris
            visit_type_results, modality_results,summary_html_categories_ris = process_ris_excel(file7_path)
            
            # Calculate totals for first table
            visit_type_totals = {
                'IP': sum(data['IP'] for data in visit_type_results.values()),
                'OP': sum(data['OP'] for data in visit_type_results.values()),
                'Emergency': sum(data['Emergency'] for data in visit_type_results.values()),
                'Total': sum(data['Total'] for data in visit_type_results.values())
            }
        
            # Calculate totals for second table
            modality_totals = {
                'XRAY': sum(data['XRAY'] for data in modality_results.values()),
                'CT Scan': sum(data['CT Scan'] for data in modality_results.values()),
                'Ultra Sound': sum(data['Ultra Sound'] for data in modality_results.values()),
                'MRI': sum(data['MRI'] for data in modality_results.values()),
                'Total': sum(data['Total'] for data in modality_results.values())
            }
            departments_ris = ["XRAY", "CT Scan", "Ultra Sound", "MRI"]
            required_ris_counts = [57, 6, 28, 3]
            ris_counts = [
                modality_totals.get('XRAY', 0),
                modality_totals.get('CT Scan', 0),
                modality_totals.get('Ultra Sound', 0),
                modality_totals.get('MRI', 0)
            ]
            df_ris = pd.DataFrame({
                'Department': departments_ris,
                'Required Count': required_ris_counts,
                'RIS Count': ris_counts
            })
            # Create enumerated list for visit_type_results
            visit_type_list = list(enumerate(visit_type_results.items(), 1))
            
            # Prepare data for visualization
            summary_table['Daily OPD Count Cleaned'] = summary_table['Daily OPD Count'].str.extract(r'>(\d+)<')[0].fillna(0).astype(int)
            
            departments = summary_table['Departments'].tolist()
            daily_opd_count = summary_table['Daily OPD Count Cleaned'].tolist()
            opd_required = summary_table['OPD Required'].tolist()

            categories = summary_table1['Patient Category'].tolist()
            patient_counts = summary_table1['Patient Count'].tolist()
            categories = categories[:-1]
            patient_counts = patient_counts[:-1]
            # LIS
            lis_categories = opd_category_table['Patient Company '].tolist()
            op_patient_counts = opd_category_table['OP Patient Count'].tolist()
            ip_patient_counts = ipd_category_table['IP Patient Count'].tolist()
            
            return render_template('file_summary.html',
    summary_html_departments=summary_html_departments,
    summary_html_categories=summary_html_categories,
    summary_html_categories_lis=summary_html_categories_lis,
    summary_html_categories_ris=summary_html_categories_ris,
    results_lis=results_lis,
    results_ot=results_ot,
    datetime=datetime.now(),
    results_biopsy=results_biopsy,
    tables=tables,
    date=file_date_str,
    summary_table=summary_table,
    summary_table1=summary_table1,
    departments_json=json.dumps(departments),  # Ensure all the variables that need to be used as JSON are passed this way
    daily_opd_count_json=json.dumps(daily_opd_count),
    opd_required_json=json.dumps(opd_required),
    categories_json=json.dumps(categories),
    patient_counts_json=json.dumps(patient_counts),
    opd_category_table=opd_category_table,
    ipd_category_table=ipd_category_table,
    
    lisCategory_json=json.dumps(lis_categories),
    opd_patient_count_json=json.dumps(op_patient_counts),
    ipd_patient_count_json=json.dumps(ip_patient_counts),
    totalCounts=json.dumps(totalCounts),  # Convert totalCounts to JSON as well
    ipd80Percent=json.dumps(ipd80Percent),  # Convert ipd80Percent to JSON
    department_names=json.dumps(department_names),  # Convert department_names to JSON
    PatientGeneral=json.dumps(PatientGeneral),  # Convert PatientGeneral to JSON
    General=json.dumps(General),  # Convert General to JSON
    
    data_dr=results_dr.to_dict('records'),
    total_count_dr=total_count_dr,
    
    visit_type_list=visit_type_list,
    modality_results=modality_results,
    visit_type_totals=visit_type_totals,
    modality_totals=modality_totals,
    df_ris=df_ris.to_dict(orient='records'),
    
    all_results_lis=all_results_lis
)

        except Exception as e:
      
            return f"Error reading or processing the Excel file: {e}", 400
    else:
        return 'File not found', 404

@app.route('/department_details/<department>/<int:file_id>', methods=['GET'])
@login_required
def department_details(department,file_id):
    try:
        # Fetch file path from the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT file1_path FROM files WHERE id = %s", (file_id,))
        file = cursor.fetchone()
        cursor.close()


        if not file:
            return "File not found", 404

        file_path = file[0]
        required_columns = [
            'Sr. No.', 'UHID', 'ABHA No.', 'Visit No.', 'Visit Date', 
            'Patient Name', 'Gender', 'Age', 
            'Consulting Doctor', 'Department', 'Patient Category', 
            'Visit Type'
        ]
        # Read the Excel file
        df = pd.read_excel(file_path, header=7)
        df.columns = df.columns.str.strip()

        # Filter data for the selected department and OP visit type
        df_filtered = df[(df['Department'] == department) & (df['Visit Type'] == 'OP')]
        df_filtered = df_filtered[required_columns]
        df_filtered = df_filtered.fillna(0) 

        # Render the data as an HTML table
        patient_details_html = df_filtered.to_html(
            index=False,
            classes='table table-bordered table-striped',
            justify='center',
            float_format="%.0f"
        )

        return render_template(
            'department_wise_patient_details.html',
            department=department,
            patient_details_html=patient_details_html,
            file_id = file_id
        )
    except Exception as e:
        return f"Error fetching details for department {department}: {e}", 400

@app.route('/preview/<int:file_id>', methods=['GET'])
@login_required
def preview_file(file_id):
   
    # Fetch file path from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT file1_path FROM files WHERE id = %s", (file_id,))
    file = cursor.fetchone()
    cursor.execute("SELECT name FROM departments")
    departments_data = cursor.fetchall()        
    cursor.close()
    # If the file does not exist in the database
    if not file:
        flash('File not found.', 'danger')
        return redirect(url_for('dashboard'))

    filepath = file[0]
    try:
        departments = [str(row[0]).strip() for row in departments_data] 
       
        # Read the Excel file
        df = pd.read_excel(filepath,header=7)
        # Strip column names to avoid whitespace issues
        df.columns = df.columns.str.strip()
        
        if 'Department' not in df.columns or 'Visit Type' not in df.columns:
                return (
                    "Required columns 'Department' or 'Visit Type' not found in the file. "
                    f"Found columns: {df.columns.tolist()}",
                    400,
                )
       
        # Define the required columns
        required_columns = [
            'Sr. No.', 'UHID', 'ABHA No.', 'Visit No.', 'Visit Date', 
            'Patient Name', 'Gender', 'Age', 
            'Consulting Doctor', 'Department', 'Patient Category', 
            'Visit Type'
        ]
        
        
         
        # Check for missing columns in the file
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            flash(f"Missing columns in the file: {', '.join(missing_columns)}", 'danger')
            return redirect(url_for('dashboard'))
        
        
        # Filter the DataFrame to only include the required columns
        df_filtered = df[df['Department'].isin(departments)]
        df_filtered=df_filtered[df_filtered['Visit Type'] == 'OP']
        df_filtered = df_filtered[required_columns]
        df_filtered = df_filtered.fillna(0) 
        # Convert the filtered DataFrame to an HTML table
        html_table = df_filtered.to_html(
            classes='table table-striped table-bordered', 
            index=False,
            float_format="%.0f"
        )
    except Exception as e:
        flash('Error reading the file: ' + str(e), 'danger')
        return redirect(url_for('dashboard'))

    # Render the preview page with the HTML table
    return render_template('preview.html', table=html_table)

@app.route('/user_stats')
def user_stats():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT u.username, us.login_time 
        FROM user_sessions us 
        JOIN users u ON us.user_id = u.id 
        ORDER BY us.login_time DESC
    """)
    user_data = cursor.fetchall()
    cursor.close()

    return render_template('user_stats.html', user_data=user_data)


@app.route('/download_login_report')
def download_login_report():
    # Fetch user data from your database
    cursor = mysql.connection.cursor()
    
    # Adjust the query to join with the users table to get the username
    cursor.execute("""
        SELECT u.username, us.login_time 
        FROM user_sessions us 
        JOIN users u ON us.user_id = u.id
    """)
    user_data = cursor.fetchall()
    cursor.close()

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(user_data, columns=['Username', 'Login Time'])

    # Split 'Login Time' into separate date and time columns
    df['Login Date'] = df['Login Time'].dt.date
    df['Login Time'] = df['Login Time'].dt.time

    # Reorganize the DataFrame to have a proper format
    df = df[['Username', 'Login Date', 'Login Time']]

    # Create an Excel workbook and add a worksheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Login Report"

    # Write the header row with formatting
    headers = ['Username', 'Login Date', 'Login Time']
    sheet.append(headers)

    # Define border style
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    # Write data rows with borders
    for index, row in df.iterrows():
        sheet.append(row.tolist())
        for cell in sheet[index + 2]:  # Start from row 2 (1-based index)
            cell.border = thin_border

    # Set alignment for all cells in the header row
    for cell in sheet[1]:
        cell.alignment = Alignment(horizontal='center')

    # Save the workbook to a BytesIO object
    excel_file_path = 'login_report.xlsx'
    workbook.save(excel_file_path)

    return send_file(excel_file_path, as_attachment=True)
@app.route('/filter_user_stats', methods=['GET'])
def filter_user_stats():
    selected_date = request.args.get('date')
    
    cursor = mysql.connection.cursor()
    
    # Adjust your query to filter by login_time
    cursor.execute("""
        SELECT u.username, us.login_time 
        FROM user_sessions us 
        JOIN users u ON us.user_id = u.id 
        WHERE DATE(us.login_time) = %s
    """, (selected_date,))
    
    user_data = cursor.fetchall()
    cursor.close()

    return render_template('user_stats.html', user_data=user_data)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



