package project;

/**
 * 
 */

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

/**
 * @author kasi
 *
 */
public class CacmQuery {

	public static HashMap<String, String> getQueries(String queryFilename)
			throws IOException {
		HashMap<String, String> queries = new HashMap<String, String>();
		String queryContents = new String(
				Files.readAllBytes(Paths.get(queryFilename)));
		Document queryFile = Jsoup.parse(queryContents);
		Elements docs = queryFile.getElementsByTag("doc");
		for (Element element : docs) {
			Element docElement = element.getElementsByTag("docno").first();
			String docno = docElement.text().trim();
			String query = docElement.nextSibling().toString().trim();
			queries.put(docno, query);
		}
		return queries;
	}

}
