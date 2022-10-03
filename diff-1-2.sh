if ! [ -d "distribution_rounds/$1" ] ; then
  echo "❌ Could not find round folder";
  echo "Usage: bash diff-1-2.sh round_folder";
  exit 1;
fi

diff <(sort "distribution_rounds/$1/distribution_results.1/raw_csv_exports/praise_aragon_distribution.csv") <(sort "distribution_rounds/$1/distribution_results.2/raw_csv_exports/praise_aragon_distribution.csv") | grep ">" | sed  s/..// > distribution_rounds/$1/praise_aragon_distribution.diff-1-2.csv