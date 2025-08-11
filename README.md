To use the programme:

1. Go to [PubMed](<https://pubmed.ncbi.nlm.nih.gov/>).
2. Search whatever terms you want.
3. Download your search with the format "Abstract (text)".
> [!TIP]
> \> Save
>
> \> (Optional) Selection: All results
>
> \> Format: Abstract (text)
5. Move the .txt file to ./in. (Create it if it doesn't exist.)
6. Change the regex strings in 'exclusion_criteria' in ./settings/setings.json to the values you want. (Optionally, change the code for the article filtering in exclusion.py to fit your needs)
7. Run main.py.
8. Results are in ./wanted/{YYYY-MM-DD}.

> [!NOTE]
> The programme is not able to handle entries that don't have a title.