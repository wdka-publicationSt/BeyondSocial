for URL in $(cut -d, -f2 < article_list | sort | uniq)
do
    wget $URL
done
