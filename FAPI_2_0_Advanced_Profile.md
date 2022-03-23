%%%
title = "FAPI 2.0 Advanced Profile"
abbrev = "fapi-2-advanced"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-advanced-00"
status = "standard"
 
[[author]]
initials="D."
surname="Fett"
fullname="Daniel Fett"
organization="yes.com"
    [author.address]
    email = "mail@danielfett.de"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub Financial Technology"
    [author.address]
    email = "dave@tonge.org"


%%%

.# Abstract 

OIDF FAPI 2.0 is an API security profile based on the OAuth 2.0
Authorization Framework [@!RFC6749].

{mainmatter}

# Introduction

## Warning

This document is not an OIDF International Standard. It is distributed
for review and comment. It is subject to change without notice and may
not be referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments,
notification of any relevant patent rights of which they are aware and
to provide supporting documentation.

## Copyright notice & license

The OpenID Foundation (OIDF) grants to any Contributor, developer,
implementer, or other interested party a non-exclusive, royalty free,
worldwide copyright license to reproduce, prepare derivative works
from, distribute, perform and display, this Implementers Draft or
Final Specification solely for the purposes of (i) developing
specifications, and (ii) implementing Implementers Drafts and Final
Specifications based on such documents, provided that attribution be
made to the OIDF as the source of the material, but that such
attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from
contributions from various sources, including members of the OpenID
Foundation and others. Although the OpenID Foundation has taken steps
to help ensure that the technology is available for distribution, it
takes no position regarding the validity or scope of any intellectual
property or other rights that might be claimed to pertain to the
implementation or use of the technology described in this
specification or the extent to which any license under such rights
might or might not be available; neither does it represent that it has
made any independent effort to identify any such rights. The OpenID
Foundation and the contributors to this specification make no (and
hereby expressly disclaim any) warranties (express, implied, or
otherwise), including implied warranties of merchantability,
non-infringement, fitness for a particular purpose, or title, related
to this specification, and the entire risk as to implementing this
specification is assumed by the implementer. The OpenID Intellectual
Property Rights policy requires contributors to offer a patent promise
not to assert certain patent claims against other contributors and
against implementers. The OpenID Foundation invites any interested
party to bring to its attention any copyrights, patents, patent
applications, or other proprietary rights that may cover technology
that may be required to practice this specification.


## Notational Conventions

The keywords "shall", "shall not",
"should", "should not", "may", and
"can" in this document are to be interpreted as described in
ISO Directive Part 2 [@!ISODIR2].
These keywords are not used as dictionary terms such that
any occurrence of them shall be interpreted as keywords
and are not to be interpreted with their natural language meanings.


# Advanced Profile

OIDF FAPI is an API security profile based on the OAuth 2.0
Authorization Framework [@!RFC6749]. This Advanced Profile aims to
reach the security goals and the non-repudiation goals laid out in the
Attacker Model [@!attackermodel].

All provisions of the [Baseline Profile] apply to the Advanced Profile
as well, with the extensions described in the following.


## Profile

In addition to the technologies used in the [Baseline Profile], the
following standards are used in the Advanced Profile:

  * OAuth 2.0 JWT Secured Authorization Request (JAR) [@!RFC9101] for signing authorization requests
  * JWT Secured Authorization Response Mode for OAuth 2.0 [@!JARM] for signing authorization responses 
  * OAuth 2.0 Token Introspection [@!RFC7662] with [@I-D.ietf-oauth-jwt-introspection-response] for signing introspection responses
  * HTTP Message Signatures [@I-D.ietf-httpbis-message-signatures] and Digest Fields [I-D.ietf-httpbis-digest-headers]
  for signing HTTP requests to and responses from Resource Servers.

We understand that some ecosystems may only desire to implement 1 or 2 of the above 3, it is therefore 
anticipated that a piece of software will be able to conform to each of the methods separately, i.e. there
will be separate tests for the following:

 * FAPI2Advanced-JAR
 * FAPI2Advanced-JARM
 * FAPI2Advanced-JIR
 * FAPI2Advanced-HTTPSig

### Signing Authorization Requests

#### Requirements for Authorization Servers

Authorization servers implementing FAPI2 authorization request signing

 1. shall support and verify signed request objects according to JAR
    [@!RFC9101] at the PAR endpoint [@!RFC9126]

#### Requirements for Clients

Clients implementing FAPI2 authorization request signing

 1. shall sign request objects according to JAR [@!RFC9101] that are sent to the PAR 
    endpoint [@!RFC9126]
 
### Signing Authorization Responses



#### Requirements for Authorization Servers

Authorization servers implementing FAPI2 authorization response signing

 1. shall support and issue signed authorization responses via JWT Secured Authorization 
    Response Mode for OAuth 2.0 [@!JARM]

#### Requirements for Clients

Clients implementing FAPI2 authorization response signing

 1. shall set the `response_mode` to `jwt` in the authorization request as defined in [@!JARM]
 2. shall verify signed authorization responses according to [@!JARM]

### Signing Introspection Responses

#### Requirements for Authorization Servers

Authorization servers implementing FAPI2 introspection response signing

 1. shall sign introspection responses that are issued in JWT format according to [@I-D.ietf-oauth-jwt-introspection-response]

#### Requirements for Clients

Clients implementing FAPI2 introspection response signing

 1. shall request signed token introspection responses according to [@I-D.ietf-oauth-jwt-introspection-response] 
 2. shall verify the signed token introspection responses


### HTTP Message Signing

This profile supports HTTP Message Signing using the *HTTP Message Signatures* specification
being developed by the IETF HTTP Working Group.

#### Requirements for Clients

Clients implementing HTTP Message Signing

 1. shall create an HTTP Message Signature as described in [I-D.ietf-httpbis-message-signatures]. 
 2. shall include `@method` (the method used in the HTTP request) in the signature input
 3. shall include `@target-uri` (the full request URI of the HTTP request) in the signature input
 4. when the message contains a request body, include the `content-digest` header as defined in 
    [I-D.ietf-httpbis-digest-headers] in the request, and include that header in the signature input. 
    Content-encoding agnostic digest methods (such as sha-256) should be used.
 5. shall accept and verify the signature in the response as described in [I-D.ietf-httpbis-message-signatures]

#### Requirements for Resource Servers

The FAPI 2.0 endpoints are OAuth 2.0 protected resource endpoints that perform sensitive actions and return protected information for the resource owner associated with the submitted access token.

Resource servers with FAPI endpoints implementing HTTP Message Signing

 1. shall verify the signature received from the Client as described in [I-D.ietf-httpbis-message-signatures]. 
 2. shall reject requests with missing or invalid signatures using HTTP Status Code 401
 3. shall create an HTTP Message Signature for the response as described in [I-D.ietf-httpbis-message-signatures].
 4. shall cryptographically link the response to the request using `@request-response` in the signature
    input as defined in 2.2.11 in [I-D.ietf-httpbis-message-signatures]
 5. shall include the `content-digest` header as defined in 
    [I-D.ietf-httpbis-digest-headers] in the response, and include that header in the signature input. 
    Content-encoding agnostic digest methods (such as sha-256) should be used.
 6. shall include `@status` (the status code of the response) in the signature input


## Acknowledgements
(todo)
     

{backmatter}

<reference anchor="attackermodel" target="https://bitbucket.org/openid/fapi/src/master/FAPI_2_0_Attacker_Model.md">
  <front>
    <title>FAPI 2.0 Attacker Model</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
   <date day="28" month="Jul" year="2021"/>
  </front>
</reference>

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

<reference anchor="OIDD" target="https://openid.net/specs/openid-connect-discovery-1_0.html">
  <front>
    <title>OpenID Connect Discovery 1.0 incorporating errata set 1</title>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura">
      <organization>NRI</organization>
    </author>
    <author initials="J." surname="Bradley" fullname="John Bradley">
      <organization>Ping Identity</organization>
    </author>
    <author initials="M." surname="Jones" fullname="Mike Jones">
      <organization>Microsoft</organization>
    </author>
    <author initials="E." surname="Jay" fullname="Edmund Jay">
      <organization>Illumila</organization>
    </author>
    <date day="8" month="Nov" year="2014"/>
  </front>
</reference>

<reference anchor="JARM" target="https://openid.net/specs/openid-financial-api-jarm.html">
  <front>
    <title>Financial-grade API: JWT Secured Authorization Response Mode for OAuth 2.0 (JARM)</title>
    <author initials="T." surname="Lodderstedt" fullname="Torsten Lodderstedt">
      <organization>Yes</organization>
    </author>
    <author initials="B." surname="Campbell" fullname="Brian Campbell">
      <organization>Ping</organization>
    </author>
   <date day="17" month="Oct" year="2018"/>
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

<reference anchor="preload" target="https://hstspreload.org/">
<front>
<title>HSTS Preload List Submission</title>
    <author fullname="Anonymous">
      <organization></organization>
    </author>
</front>
</reference>

