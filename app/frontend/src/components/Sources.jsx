function Sources({ sources }) {

  if (
    !sources ||
    sources.length === 0
  ) {
    return null;
  }


  return (
    <div className="sources">

      <div className="sources-title">
        المصادر المستخدمة
      </div>


      <div className="sources-list">

        {sources.map((source) => (

          <div
            className="source"
            key={source.id}
          >

            <div className="source-number">
              {source.id}
            </div>


            <div className="source-info">

              <span className="source-name">
                {source.filename}
              </span>


              {source.chunk_ids?.length > 0 && (

                <span className="source-meta">
                  {
                    source.chunk_ids.length
                  }
                  {" "}
                  chunk
                </span>

              )}

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}


export default Sources;