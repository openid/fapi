%%%
title = "FAPI 2.0 Advanced Authorization Profile"
abbrev = "fapi-2_0-advanced-authorization"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-advanced-authorization-01"
status = "standard"

[[author]]
initials="R."
surname="Bragg"
fullname="Ralph Bragg"
organization="Raidiam"
    [author.address]
    email = "ralph.bragg@raidiam.com"

[[author]]
initials="T."
surname="Lodderstedt"
fullname="Torsten Lodderstedt"
organization="yes.com"
    [author.address]
    email = "torsten@lodderstedt.net"
	
[[author]]
initials="S."
surname="Low"
fullname="Stuart Low"
organization="Biza.io"
    [author.address]
    email = "stuart@biza.io"

[[author]]
initials="D."
surname="Postnikov"
fullname="Dima Postnikov"
    [author.address]
    email = "dima@postnikov.net"
    


%%%

.# Abstract 

The Financial-grade API (FAPI) 2.0 Advanced Authorization profile is... 

{mainmatter}

# Introduction
Financial-grade API (FAPI) 2.0 2.0 Advanced Authorization profile...

## Warning

This document is not an OIDF International Standard. It is distributed for
review and comment. It is subject to change without notice and may not be
referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments,
notification of any relevant patent rights of which they are aware and to
provide supporting documentation.

## Copyright notice & license

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer,
or other interested party a non-exclusive, royalty free, worldwide copyright
license to reproduce, prepare derivative works from, distribute, perform and
display, this Implementers Draft or Final Specification solely for the purposes
of (i) developing specifications, and (ii) implementing Implementers Drafts and
Final Specifications based on such documents, provided that attribution be made
to the OIDF as the source of the material, but that such attribution does not
indicate an endorsement by the OIDF.

The technology described in this specification was made available from
contributions from various sources, including members of the OpenID Foundation
and others. Although the OpenID Foundation has taken steps to help ensure that
the technology is available for distribution, it takes no position regarding the
validity or scope of any intellectual property or other rights that might be
claimed to pertain to the implementation or use of the technology described in
this specification or the extent to which any license under such rights might or
might not be available; neither does it represent that it has made any
independent effort to identify any such rights. The OpenID Foundation and the
contributors to this specification make no (and hereby expressly disclaim any)
warranties (express, implied, or otherwise), including implied warranties of
merchantability, non-infringement, fitness for a particular purpose, or title,
related to this specification, and the entire risk as to implementing this
specification is assumed by the implementer. The OpenID Intellectual Property
Rights policy requires contributors to offer a patent promise not to assert
certain patent claims against other contributors and against implementers. The
OpenID Foundation invites any interested party to bring to its attention any
copyrights, patents, patent applications, or other proprietary rights that may
cover technology that may be required to practice this specification.


## Notational Conventions

The keywords "shall", "shall not", "should", "should not", "may", and "can" in
this document are to be interpreted as described in ISO Directive Part 2
[@!ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.

# Advanced Authorization Profile

OIDF FAPI is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749]. This Baseline Profile aims to reach the security goals
laid out in the Attacker Model [@!attackermodel].

Fine grain authorization

Clients managing grants 

## Use cases 

## Profile

In the following, a profile of the following technologies is defined:

  * OAuth 2.0 Rich Authorization Requests (RAR) [@!I-D.ietf-oauth-rar]
  * Grant Management for OAuth 2.0 []

  
### Requirements for Authorization Servers

Authorization servers
 
 1. shall support the authorization_details parameter according to [@!I-D.ietf-oauth-rar]. 
 2. shall support Grant Management APIs according to [] 

### Requirements for Clients

Clients

 1. shall use the authorization_details parameter according to [@!I-D.ietf-oauth-rar] to convey the authorization clients want to obtain if the scope parameter is not expressive enough for that purpose.
 2. shall use Grant Management when client is required to support concurrent grants. 

### Requirements for Resource Servers

The FAPI 2.0 endpoints are OAuth 2.0 protected resource endpoints that return
protected information for the resource owner associated with the submitted
access token.

Resource servers with the FAPI endpoints

1. shall enforce API authorization based on authorization_details. NOTE: To be discussed if this is required.

### Requirements for Conformance Test

Conformance test:

1.

                                           |                                                                                                       |
## Acknowledgements

We would like to thank ... for their valuable feedback and contributions that helped to evolve this specification.

{backmatter}

<reference anchor="OIDC" target="http://openid.net/specs/openid-connect-core-1_0.html">
  <front>
    <title>OpenID Connect Core 1.0 incorporating errata set 1</title>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura">
      <organization>NRI</organization>
    </author>
    <author initials="J." surname="Bradley" fullname="John Bradley">
      <organization>Ping Identity</organization>
    </author>
    <author initials="M." surname="Jones" fullname="Mike Jones">
      <organization>Microsoft</organization>
    </author>
    <author initials="B." surname="de Medeiros" fullname="Breno de Medeiros">
      <organization>Google</organization>
    </author>
    <author initials="C." surname="Mortimore" fullname="Chuck Mortimore">
      <organization>Salesforce</organization>
    </author>
   <date day="8" month="Nov" year="2014"/>
  </front>
</reference>

<reference anchor="ISODIR2" target="https://www.iso.org/sites/directives/current/part2/index.xhtml">
<front>
<title>ISO/IEC Directives Part 2 - </title>
    <author fullname="International Organization for Standardization">
      <organization></organization>
    </author>
</front>
</reference>

# Notices

Copyright (c) 2021 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.