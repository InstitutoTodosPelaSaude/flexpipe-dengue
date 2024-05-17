# -*- coding: utf-8 -*-

import pycountry_convert as pyCountry
import pycountry
import pandas as pd
import argparse
#from uszipcode import SearchEngine


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Reformat metadata file by adding column with subcontinental regions based on the UN geo-scheme",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--metadata", required=True, help="Nextstrain metadata file")
    parser.add_argument("--geoscheme", required=True, help="XML file with geographic classifications")
    parser.add_argument("--output", required=True, help="Updated metadata file")
    args = parser.parse_args()

    metadata = args.metadata
    geoscheme = args.geoscheme
    output = args.output

    # path = '/Users/anderson/GLab Dropbox/Anderson Brito/ITpS/projetos_itps/dashboard/nextstrain/run5_20210920_template/'
    # metadata = path + 'pre-analyses/metadata_filtered.tsv'
    # geoscheme = path + 'config/geoscheme.tsv'
    # output = path + 'pre-analyses/metadata_geo.tsv'



    def load_table(file):
        df = ''
        if str(file).split('.')[-1] == 'tsv':
            separator = '\t'
            df = pd.read_csv(file, encoding='utf-8', sep=separator, dtype='str')
        elif str(file).split('.')[-1] == 'csv':
            separator = ','
            df = pd.read_csv(file, encoding='utf-8', sep=separator, dtype='str')
        elif str(file).split('.')[-1] in ['xls', 'xlsx']:
            df = pd.read_excel(file, index_col=None, header=0, sheet_name=0, dtype='str')
            df.fillna('', inplace=True)
        else:
            print('Wrong file format. Compatible file formats: TSV, CSV, XLS, XLSX')
            exit()
        return df


    # get ISO alpha3 country codes
    isos = {}
    def get_iso(country):
        global isos
        if country not in isos.keys():
            try:
                isoCode = pyCountry.country_name_to_country_alpha3(country, cn_name_format="default")
                isos[country] = isoCode
            except:
                try:
                    isoCode = pycountry.countries.search_fuzzy(country)[0].alpha_3
                    isos[country] = isoCode
                except:
                    isos[country] = ''
        return isos[country]

    # parse subcontinental regions in geoscheme
    dfS = load_table(geoscheme)
    geoLevels = {}
    c = 0    

    # open metadata file as dataframe
    dfN = pd.read_csv(metadata, encoding='utf-8', sep='\t')
    
    # Find the position of columns mentioned in dfS['member_type'] in dfN
    col_positions = {}
    for member_type in dfS['member_type'].unique():
        if member_type in dfN.columns:
            if member_type not in col_positions.keys():
                colpos = dfN.columns.get_loc(member_type)
                col_positions[member_type] = colpos
        else:
            print(f'Column {member_type} does not exist in metadata file. Fix the geoscheme file to match the metadata file.')
            exit()


    new_columns = {}
    # iterate over the geoscheme file
    for idx, row in dfS.iterrows():
        member_type = dfS.loc[idx, 'member_type']
        newcol = dfS.loc[idx, 'newcol']
        categories = dfS.loc[idx, 'categories']
        members = dfS.loc[idx, 'members'].split(',')  # elements inside the category 

        # parse countries in geoscheme
        if member_type == 'country':
            if newcol not in dfN.columns:
                dfN.insert(col_positions[member_type], newcol, '')
                new_columns[member_type] = newcol
                
            for country in members:
                iso = get_iso(country.strip())
                geoLevels[iso] = categories

        # parse subnational regions for countries in geoscheme
        if member_type == 'division':
            if newcol not in dfN.columns:
                dfN.insert(col_positions[member_type], newcol, '')
                new_columns[member_type] = newcol
            else:
                pass
                # print('Column ' + newcol + ' already exists in metadata file. Choose another column name and fix the geoscheme file.')

            for state in members:
                if state.strip() not in geoLevels.keys():
                    geoLevels[state.strip()] = categories

        for elem in members:
            if elem.strip() not in geoLevels.keys():
                geoLevels[elem.strip()] = categories

    print
    if 'country' in new_columns.keys():
        pos = dfN.columns.get_loc('country')
        dfN.insert(pos, 'code', '')
        dfN['code'] = dfN['country'].apply(lambda x: get_iso(x))
        dfN[new_columns['country']] = dfN['code'].map(geoLevels)

    if 'division' in new_columns.keys():
        dfN[new_columns['division']] = ''


    # convert sets of locations into sub-locations
    print('\nApplying geo-schemes...')
    dfN.fillna('', inplace=True)

    for idx, row in dfN.iterrows():
        country = dfN.loc[idx, 'country']

        # assign BR region
        if country not in ['Brazil']:
            dfN.loc[idx, new_columns['division']] = 'Other'

        if country == 'Brazil' and dfN.loc[idx, new_columns['division']] == '':
            division = dfN.loc[idx, 'division']
            if division not in ['', 'unknown']:
                if division in geoLevels.keys():
                    dfN.loc[idx, new_columns['division']] = geoLevels[dfN.loc[idx, 'division']]
                else:
                    dfN.loc[idx, new_columns['division']] = 'Other'

        # # divide country into subnational regions
        # division = dfN.loc[idx, 'division']
        # if division not in ['', 'unknown']:
        #     if division in geoLevels.keys():
        #         # print('Found ' + division + ' in geo-scheme')
        #         dfN.loc[idx, 'country'] = geoLevels[dfN.loc[idx, 'division']]

        # print('Processing metadata for... ' + row['strain'])

    dfN = dfN.drop_duplicates(subset=['strain'])
    dfN.to_csv(output, sep='\t', index=False)

print('\nMetadata file successfully reformatted applying geo-scheme!\n')
