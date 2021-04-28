%%%
title = "FAPI 2.0 Attacker Model"
abbrev = "fapi-2_0-attacker-model"
ipr = "trust200902"
workgroup = "connect"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-attacker-model-00"
status = "standard"

[[author]]
initials="D."
surname="Fett"
fullname="Daniel Fett"
organization="yes.com"
    [author.address]
    email = "mail@danielfett.de"


%%%

.# Abstract 

OIDF FAPI 2.0 is an API security profile suitable for high-security
applications based on the OAuth 2.0 Authorization Framework
[@!RFC6749]. This document describes that attacker model that informs
the decisions on security mechanisms employed by the FAPI security
profiles.



{mainmatter}

# Introduction

Since OIDF FAPI aims at providing an API protection profile for high-risk
scenarios, clearly defined security requirements are indispensable. In this
document, the security requirements are expressed through attacker models,
security goals, and non-repudiation requirements. From these requirements, the
utilized security mechanisms are derived in the Baseline and Advanced profiles.

The ultimate aim is to provide systematic proofs of the security of the FAPI
profiles similar to those in [@arXiv.1901.11520]. Formal proofs can rule out
large classes of attacks rooted in the logic of security protocols. Until such
proofs are provided for FAPI, the attacker model laid out herein informs the
design decisions for FAPI, but, as with most security protocols, there is no
guarantee that all attacks for all types of attackers are excluded.

The security requirements in this document are expressed in a form that lends
itself well to a transfer into a formal representation required for an automated
or manual analysis of the security of FAPI. This work draws from the attacker
model and security goals formulated in [@arXiv.1901.11520].

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

The keywords "shall", "shall not", "should", "should not", "may", and "can" in
this document are to be interpreted as described in ISO Directive Part 2
[@!ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.


# Security Goals

FAPI 2.0 profiles aim to achieve at least the following security goals
(with respect to the attacker models defined below):

## Authorization
FAPI 2.0 profiles shall ensure that **no attacker can access resources
belonging to a user.**

The access token is the ultimate credential for access to resources in
OAuth. Therefore, this security goal is fulfilled if no attacker can
successfully obtain and use an access token belonging to a user.

## Authentication

FAPI 2.0 profiles shall ensure that **no attacker is able to log in at
a client under the identity of a user.**

The ID token is the credential for authentication in OpenID Connect.
This security goal therefore is fulfilled if no attacker can obtain
and use an ID token carrying the identity of a user for login.


## Session Integrity
Session Integrity is concerned with attacks where a user is tricked
into logging in under the attacker’s identity or inadvertently using
the resources of the attacker instead of the user’s own resources.
Attacks in this field include CSRF attacks (traditionally defended
against by using “state” in OAuth) and session swapping attacks.

In detail:

  * For authentication: FAPI 2.0 profiles shall ensure that **no
    attacker is able to force a user to be logged in under the
    identity of the attacker.**
  * For authorization: FAPI 2.0 profiles shall ensure that **no
    attacker is able to force a user to use resources of the
    attacker.**

# Attacker Model 

## Assumptions

This attacker model assumes that certain parts of the infrastructure
are working correctly. Failures in these parts likely lead to attacks
that are out of the scope of this attacker model and shall be
considered and analyzed separately.

For example, if a major flaw in TLS was found that undermines data integrity in
TLS connections, a network attacker (A2, below) would be able to compromise
practically all OAuth and OpenID Connect sessions in various ways. This would be
fatal, as even application-level signing and encryption is based on key
distribution via TLS connections. As another example, if a human error leads to
the disclosure of secret keys for authentication and an attacker would be able
to misuse these credentials, this attack would not be covered by this attacker
model.

The following parts of the infrastructure are out of the scope of this
attacker model:

  * **TLS:** It is assumed that TLS connections are not broken, i.e.,
    data integrity and confidentiality are ensured. The correct public
    keys are used to establish connections and private keys are not
    known to attackers (except for explicitly compromised parties).
  * **JWKS:** Where applicable, key distribution mechanisms work as
    intended, i.e., encryption and signature verification keys of
    uncompromised parties are retrieved from the correct endpoints.
  * **Browsers and Endpoints:** Devices and
    browsers used by resource owners are considered not compromised. Other
    endpoints not controlled by an attacker behave according to the
    protocol.

## Attackers

FAPI 2.0 profiles aim to ensure the security goals listed above for arbitrary
combinations of the following attackers, potentially collaborating to reach a
common goal:


### A1 - Web Attacker

Standard web attacker model. Can send and receive messages just like any other
party controlling one or more endpoints on the internet. Can participate in
protocols flows as a normal user. Can use arbitrary tools (e.g., browser
developer tools, custom software, local interception proxies) on their own
endpoints to tamper with messages and assemble new messages. Can send links to
honest users that are then visited by these users. This means that the web
attacker has the ability to cause, arbitrary requests from users' browsers, as
long as the contents are known to the attacker.

Cannot intercept or block messages sent between other parties, and cannot break
cryptography unless the attacker has learned the respective decryption keys.
Deviating from the common web attacker model, A1 cannot play the role of a
legitimate AS in the ecosystem (see A1a).

### A1a - Web Attacker (participating as AS)

Like the web attacker A1, but can also participate as an AS in the ecosystem.
Note that this AS can reuse/replay messages it has received from honest ASs and
can send users to endpoints of honest ASs.

### A2 - Network attacker

Controls the whole network (like a rogue WiFi access point or any other
compromised network node). Can intercept, block, and tamper with messages
intended for other people, but cannot break cryptography unless the attacker has
learned the respective decryption keys. 

Note: Most attacks that are exclusive to this kind of attacker can be defended
against by using transport layer protection like TLS.

### Attackers at the Authorization Endpoint

**Note:** The attackers for the authorization request are more
fine-grained than those for the token endpoint and resource endpoint,
since these messages pass through the complex environment of the
user's browser/app/OS with a larger attack surface. This demands for a
more fine-grained analysis.

#### A3a - Read Authorization Request

The capabilities of the web attacker, but can also read the authorization
request sent in the front channel from a user's browser to the authorization
server. This might happen on mobile operating systems (where apps can register
for URLs), on all operating systems through the browser history, or due to
Cross-Site Scripting on the AS. There have been cases where anti-virus software
intercepts TLS connections and stores/analyzes URLs.

#### A3b - Read Authorization Response

The capabilities of the web attacker, but can also read the authorization
response. This can happen e.g., due to the URL leaking in proxy logs, web
browser logs, web browser history, or on mobile operating systems.

### Attackers at the Token Endpoint

#### A5 - Read and Tamper with Token Requests and Responses

This attacker makes the client use a token endpoint that is not the one of the
honest AS. This attacker can read and tamper with messages sent to and from this
token endpoint that the client thinks as of an honest AS.

Note: When the token endpoint address is obtained from an authoritative source and via a protected channel, e.g., through OAuth Metadata obtained from the honest AS, this attacker is not relevant.

### Attackers at the Resource Server

#### A7 - Read Resource Requests and Responses

The capabilities of the web attacker, but this attacker can also read requests
sent to and from the resource server, for example because the attacker can read
TLS intercepting proxy logs on the RS's side.

#### A8 - Tamper with Resource Responses

The capabilities of A7, but this attacker can also tamper with responses from
the resource servers (e.g., a compromised reverse proxy in front of the resource
server). 



# Non-Repudiation Requirements

Beyond what is captured by the security goals and the attacker model, parties
could try to deny having sent a particular message, for example, a payment
request. For this purpose, non-repudiation is needed. This is usually achieved
by providing application-level signatures that can be stored together with the
payload and meaningful metadata of a request or response. 

## Affected messages

  * NR1: Pushed Authorization Requests
  * NR2: Responses to Pushed Authorization Requests
  * NR3: Authorization Requests (Front-Channel)
  * NR4: Authorization Responses (Front-Channel)
  * NR5: ID Token Contents
  * NR6: Introspection Responses
  * NR7: Userinfo Responses
  * NR8: Resource Requests
  * NR9: Resource Responses


{backmatter}

<reference anchor="OpenID" target="http://openid.net/specs/openid-connect-core-1_0.html">
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


<reference anchor="arXiv.1901.11520"
           target="http://arxiv.org/abs/1901.11520/">
  <front>
    <title>An Extensive Formal Security Analysis of the OpenID Financial-grade API</title>
    <author fullname="Daniel Fett" surname="Fett" initials="D."><organization/></author>
    <author fullname="Pedram Hosseyni" surname="Hosseyni" initials="P."><organization/></author>
    <author fullname="Ralf Küsters" surname="Küsters" initials="R."><organization/></author>
    <date day="31" month="January" year="2019"/>
  </front>
  <seriesInfo name="arXiv" value="1901.11520"/>
</reference>
