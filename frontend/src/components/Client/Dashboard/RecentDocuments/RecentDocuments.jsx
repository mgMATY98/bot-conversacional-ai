import { FileText, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

import Card from "../../../Card/card";

import "./RecentDocuments.css";

function RecentDocuments({

    documents = [],

    loading

}) {

    return (

        <Card>

            <div className="widget-header">

                <h3>

                    Documentos recientes

                </h3>

                <Link

                    to="/client/documents"

                    className="widget-link"

                >

                    Ver todos

                    <ArrowRight size={16} />

                </Link>

            </div>

            {

                loading

                    ?

                    (

                        <div className="widget-loading">

                            Cargando...

                        </div>

                    )

                    :

                    documents.length === 0

                        ?

                        (

                            <div className="widget-empty">

                                No hay documentos.

                            </div>

                        )

                        :

                        (

                            documents.map((document) => (

                                <Link

                                    key={document.id}

                                    to="/client/documents"

                                    className="document-item"

                                >

                                    <div className="document-icon">

                                        <FileText size={18} />

                                    </div>

                                    <div className="document-content">

                                        <strong>

                                            {document.name}

                                        </strong>

                                        <span>

                                            {document.uploaded_at}

                                        </span>

                                    </div>

                                </Link>

                            ))

                        )

            }

        </Card>

    );

}

export default RecentDocuments;